import streamlit as st
import datetime
from todo import TodoDB
# 패키지 설치 email-validator
from email_validator import validate_email, EmailNotValidError
import re
import pandas as pd

# DB 객체 생성
db = TodoDB()
# DB 연결
TodoDB.connectToDatabase()

# streamlit 설정: layout="wide" -> 넓은 화면 사용
st.set_page_config(layout="wide")

# 사이드 바 생성
sb = st.sidebar

# 사이드바에 선택상자를 메뉴로 사용
menu = sb.selectbox('메뉴', ['회원가입', '할일', '통계', '검색'])

if menu == '회원가입':

    # 컬럼 레이아웃 생성
    ucol1, ucol2 = st.columns([6, 6]) # st.columns(2)와 같음

    with ucol1: # 첫번째 칼럼

        st.subheader('회원가입')

        # 회원가입 입력 폼 시작
        with st.form(key='user_reg', clear_on_submit=True):
            user_name = st.text_input('성명', max_chars=12)
            user_gender = st.radio('성별', options=('남', '여'), horizontal=True)
            user_id = st.text_input('아이디', max_chars=12)
            col1, col2 = st.columns(2)
            user_pw = col1.text_input('비밀번호', max_chars=12, type='password')
            user_pw_chk = col2.text_input('비밀번호 확인', max_chars=12, type='password')
            user_email = st.text_input('이메일')
            user_mobile = st.text_input('휴대전화', placeholder='하이픈(-) 포함 할 것')

            submit = st.form_submit_button('가입') # st.form 과 한 쌍으로 작동
            if submit: # 가입 버튼을 클릭하면
                # 이름 한글 검증
                if re.compile('[가-힣]+').sub('', user_name):
                    st.error('성명은 한글만 입력해야 합니다.')
                    st.stop()
                # 아이디 검증
                if re.compile('[a-zA-Z0-9]+').sub('', user_id):
                    st.error('아이디는 영문자와 숫자만 입력해야 합니다.')
                    st.stop()

                # 비밀번호 확인
                if user_pw != user_pw_chk:
                    st.error('비밀번호가 일치하지 않습니다.')
                    st.stop()

                # 이메일 검증
                try:
                    user_email = validate_email(user_email).email

                except EmailNotValidError as e:
                    st.error(str(e))
                    st.stop()
                # 휴대전화 검증
                regex = re.compile('^(01)\d{1}-\d{3,4}-\d{4}$')
                phone_validation = regex.search(user_mobile.replace(' ', ''))
                if not phone_validation:
                    st.error('전화번호 형식이 올바르지 않습니다.')
                    st.stop()

                # 데이터베이스에 사용자 정보 입력
                db.insertUser((
                    user_name, user_gender, user_id, user_pw, user_email,
                    user_mobile, str(datetime.datetime.now())
                ))

    with ucol2:  # 두번째 칼럼

        st.subheader('회원목록')

        # 데이터베이스에서 회원 정보 가져오기
        users = db.readUsers()

        def delete_user(*args, **kargs):
            db.deleteUser(args[0])


        for user in users:

            title = user[1]+'('+ user[3] + ')'
            with st.expander(title):
                st.write(f'{user[1]}({user[5]})')
                st.write(f'{user[2]}')
                st.write(f'{user[6]}')
                st.write(f'{user[7][:19]}')
                st.button('삭제', on_click=delete_user, args=(user[0],), key='del'+str(user[0]))

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
        db.insertTodo((
            todo_content,
            todo_date.strftime('%Y-%m-%d'),
            todo_time.strftime('%H:%M'),
            completed,
            str(datetime.datetime.now())))
        # 화면 새로고침
        st.experimental_rerun()

    st.subheader('할일목록')

    # 콜백함수들 정의
    def change_state(*args, **kargs):
        db.updateTaskState(args)

    def change_content(*args, **kargs):
        db.updateTodoContent((args[0], st.session_state[args[1]]))

    def change_date(*args, **kargs):
        db.updateTodoDate((args[0], st.session_state[args[1]].strftime('%Y-%m-%d')))

    def change_time(*args, **kargs):
        db.updateTodoTime((args[0], st.session_state[args[1]].strftime('%H:%M')))

    def delete_todo(*args, **kargs):
        # print(type(args[0]))
        db.deleteTodo(args[0])

    # 데이터베이스에서 할 일 데이터 가져오기
    todos = db.readTodos()
    for todo in todos:
        col1, col2, col3, col4, col5, col6 = st.columns([1,3,2,2,3,2])
        col1.checkbox(
            str(todo[0]),
            value=True if todo[4] else False,
            on_change=change_state,
            label_visibility='collapsed',
            args=(todo[0], False if todo[4] else True))
        col2.text_input(
            str(todo[0]),
            value=todo[1],
            on_change=change_content,
            label_visibility='collapsed',
            args=(todo[0], 'content'+str(todo[0])),
            key='content'+str(todo[0]))
        col3.date_input(
            str(todo[0]),
            value=datetime.datetime.strptime(todo[2], '%Y-%m-%d').date(),
            on_change=change_date,
            label_visibility='collapsed',
            args=(todo[0], 'date'+str(todo[0])),
            key='date'+str(todo[0]))
        col4.time_input(
            str(todo[0]),
            value=datetime.datetime.strptime(todo[3], '%H:%M').time(),
            on_change=change_time,
            label_visibility='collapsed',
            args=(todo[0], 'time'+str(todo[0])),
            key='time'+str(todo[0]))
        col5.text(todo[5][0:19])
        col6.button(
            '삭제',
            on_click=delete_todo,
            args=(todo[0], ),
            key='del' + str(todo[0])
            )

elif menu == '통계':

    st.subheader('통계')

    users = db.readUsers()
    todos = db.readTodos()

    col1, col2 = st.columns([5,5])

    df_users = pd.DataFrame(users, columns=['id','성명','성별','아이디','비밀번호','이메일','휴대전화','등록일시']).set_index('id')
    df_todos = pd.DataFrame(todos, columns=['id','할일','날짜','시간','완료여부','등록일시']).set_index('id')

    with col1:
        st.markdown('#### 회원')
        st.dataframe(df_users, use_container_width=True)

        st.markdown('##### 회원 요약')
        st.dataframe(df_users.describe(include='all').fillna("").astype('str'), use_container_width=True)

        st.markdown('##### 성별 인원')
        df_sex = df_users['성별'].value_counts()
        st.dataframe(df_sex)

        from collections import Counter
        df_sex2 = Counter(df_users['성별'])
        st.dataframe(df_sex2)


    with col2:
        st.markdown('#### 할일')
        st.dataframe(df_todos, use_container_width=True)

        st.markdown('##### 할일 요약')
        st.dataframe(df_todos.describe(include='all').fillna("").astype('str'), use_container_width=True)

        st.markdown('##### 조건 검색')
        df_date = df_todos.loc[df_todos['날짜'] >= '2023-04-10'][['할일','날짜','시간']]
        st.dataframe(df_date, use_container_width=True)

elif menu == '검색':

    with st.sidebar:
        # 회원검색
        st.subheader('회원검색')
        s_name = st.text_input('성명')
        s_btn = st.button('회원검색')

        # 할일검색
        st.subheader('할일검색')
        t_name = st.text_input('할일')
        t_date = st.text_input('날짜')
        t_btn = st.button('할일검색')

    if s_btn:
        res = db.findUserByName(s_name)
        st.subheader('검색 결과')
        st.dataframe(res)

    if t_btn:
        res = db.findTodos(t_name, t_date)
        st.subheader('검색 결과')
        st.dataframe(res)