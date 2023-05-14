import streamlit as st
import datetime
from todo_firebase import DB
# 패키지 설치 email-validator
from email_validator import validate_email, EmailNotValidError
import re
import pandas as pd

# DB 객체 생성
db = DB()
# DB 연결
DB.connect_db()

# streamlit 설정: layout="wide" -> 넓은 화면 사용
st.set_page_config(layout="wide")

# 사이드 바 생성
sb = st.sidebar

# 사이드바에 선택상자를 메뉴로 사용
menu = sb.selectbox('메뉴', ['회원가입', '할일', '통계'])

if menu == '회원가입':

    # 컬럼 레이아웃 생성
    ucol1, ucol2 = st.columns([6, 6]) # st.columns(2)와 같음

    with ucol1: # 첫번째 칼럼

        st.subheader('회원가입')

        # 회원가입 입력 폼 시작
        with st.form(key='user_reg'):
            user_name = st.text_input('성명', max_chars=12, key='user_name')
            user_gender = st.radio('성별', options=('남', '여'), horizontal=True, key='user_gender')
            user_id = st.text_input('아이디', max_chars=12, key='user_id')
            col1, col2 = st.columns(2)
            user_pw = col1.text_input('비밀번호', max_chars=12, type='password', key='user_pw')
            user_pw_chk = col2.text_input('비밀번호 확인', max_chars=12, type='password', key='user_pw_chk')
            user_email = st.text_input('이메일', key='user_email')
            user_mobile = st.text_input('휴대전화', placeholder='하이픈(-) 포함 할 것', key='user_mobile')

            submit = st.form_submit_button('저장') # st.form 과 한 쌍으로 작동
            if submit: # 가입 버튼을 클릭하면
                print(st.session_state)
                u_name = st.session_state['user_name']
                u_gender = st.session_state['user_gender']
                u_id = st.session_state['user_id']
                u_pw = st.session_state['user_pw']
                u_email = st.session_state['user_email']
                u_mobile = st.session_state['user_mobile']
                print('u_name', u_name)

                flag = True
                # 이름 한글 검증

                if len(u_name) < 2:
                    flag = False
                    st.error('성명은 적어도 2글자 이상이어야 합니다.')

                if re.compile('[가-힣]+').sub('', u_name):
                    st.error('성명은 한글만 입력해야 합니다.')
                    flag = False
                # 아이디 검증
                if re.compile('[a-zA-Z0-9]+').sub('', u_id):
                    st.error('아이디는 영문자와 숫자만 입력해야 합니다.')
                    flag = False

                # 비밀번호 확인
                if u_pw != user_pw_chk:
                    st.error('비밀번호가 일치하지 않습니다.')
                    flag = False

                try:
                    u_email = validate_email(u_email).email

                except EmailNotValidError as e:
                    print(u_email)
                    st.error(e)
                    flag = False
                # 휴대전화 검증
                regex = re.compile('^(01)\d{1}-\d{3,4}-\d{4}$')
                phone_validation = regex.search(u_mobile.replace(' ', ''))
                if not phone_validation:
                    st.error('전화번호 형식이 올바르지 않습니다.')
                    flag = False

                if flag:
                    # 데이터베이스에 사용자 정보 입력

                    if 'id' not in st.session_state:
                        db.insert_user(
                            {
                                'user_name': u_name,
                                'user_gender': u_gender,
                                'user_id': u_id,
                                'user_pw': u_pw,
                                'user_email': u_email,
                                'user_mobile': u_mobile,
                                'reg_date': str(datetime.datetime.now())
                            })
                    else:
                        db.update_user(
                            st.session_state['id'],
                            {
                                'user_name': u_name,
                                'user_gender': u_gender,
                                'user_id': u_id,
                                'user_pw': u_pw,
                                'user_email': u_email,
                                'user_mobile': u_mobile
                            })
                        del st.session_state['id']
                        st.experimental_rerun()

    with ucol2:  # 두번째 칼럼

        st.subheader('회원목록')

        # 데이터베이스에서 회원 정보 가져오기
        users = db.read_users()

        def delete_user(*args, **kargs):
            db.delete_user(args[0])

        def update_user(*args, **kargs):
            id = args[0]
            user = args[1]
            print(user)
            st.session_state['id'] = id
            st.session_state['user_name'] = user['user_name']
            st.session_state['user_id'] = user['user_id']
            st.session_state['user_pw'] = user['user_pw']
            st.session_state['user_pw_chk'] = user['user_pw']
            st.session_state['user_gender'] = user['user_gender']
            st.session_state['user_email'] = user['user_email']
            st.session_state['user_mobile'] = user['user_mobile']
            print(st.session_state)

        if users is not None:

            for id, user in users.items():

                title = user['user_name']+'('+ user['user_gender'] + ')'
                with st.expander(title):
                    st.write(f"{user['user_name']}({user['user_id']})")
                    st.write(f"{user['user_email']}")
                    st.write(f"{user['user_mobile']}")
                    st.write(f"{user['reg_date'][:19]}")
                    bcol1, bcol2, bcol3 = st.columns([2,2,8])
                    bcol1.button('수정', on_click=update_user, args=(id, user), key='update'+id)
                    bcol2.button('삭제', on_click=delete_user, args=(id,), key='del'+id)

elif menu == '할일':

    st.subheader('할일입력')

    # 할일 입력 폼
    # 내용, 날짜, 추가 버튼
    todo_content = st.text_input('할 일', placeholder='할 일을 입력하세요.')
    col1, col2, col3 = st.columns([2, 2, 2])
    todo_date = col1.date_input('날짜')
    todo_time = col2.time_input('시간')
    completed = st.checkbox('완료')
    btn = st.button('추가')

    if btn: # 추가 버튼을 클릭했을 때

        # 데이터베이스에 할 일 입력
        db.insert_todo(
            {
                'todo_content': todo_content,
                'todo_date': todo_date.strftime('%Y-%m-%d'),
                'todo_time': todo_time.strftime('%H:%M'),
                'completed': completed,
                'reg_date': str(datetime.datetime.now())
            })
        # 화면 새로고침
        st.experimental_rerun()

    st.subheader('할일목록')

    # 콜백함수들 정의
    def change_state(*args, **kargs):
        db.update_task_state(args[0], {'completed': st.session_state['completed'+args[0]]})

    def change_content(*args, **kargs):
        print(args[0], args[1])
        db.update_task_state(args[0], {'todo_content': st.session_state['todo_content'+args[0]]})

    def change_date(*args, **kargs):
        db.update_task_state(args[0], {'todo_date': st.session_state['todo_date'+args[0]].strftime('%Y-%m-%d')})

    def change_time(*args, **kargs):
        db.update_task_state(args[0], {'todo_time': st.session_state['todo_time'+args[0]].strftime('%H:%M')})

    def delete_todo(*args, **kargs):
        # print(type(args[0]))
        db.delete_todo(args[0])

    # 데이터베이스에서 할 일 데이터 가져오기
    todos = db.read_todos()

    if todos is not None:
        for id, todo in todos.items():
            col1, col2, col3, col4, col5, col6 = st.columns([1,3,2,2,3,2])
            col1.checkbox(
                id,
                value=True if todo['completed'] else False,
                on_change=change_state,
                label_visibility='collapsed',
                args=(id, False if todo['completed'] else True),
                key='completed'+id
            )
            col2.text_input(
                id,
                value=todo['todo_content'],
                on_change=change_content,
                label_visibility='collapsed',
                args=(id, f"{todo['todo_content']}"),
                key='todo_content'+id)
            col3.date_input(
                id,
                value=datetime.datetime.strptime(todo['todo_date'], '%Y-%m-%d').date(),
                on_change=change_date,
                label_visibility='collapsed',
                args=(id, f"{todo['todo_date']}"),
                key='todo_date'+id)
            col4.time_input(
                id,
                value=datetime.datetime.strptime(todo['todo_time'], '%H:%M').time(),
                on_change=change_time,
                label_visibility='collapsed',
                args=(id, f"{todo['todo_time']}"),
                key='todo_time'+id)
            col5.text(todo['reg_date'][0:19])
            col6.button(
                '삭제',
                on_click=delete_todo,
                args=(id, ),
                key='del' + id
                )
