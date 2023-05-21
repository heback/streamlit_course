import streamlit as st
import datetime
from todo_firebase import DB, Auth

# DB 객체 생성
db = DB()
# DB 연결
DB.connect_db()

st.set_page_config(layout="centered")

# 사이드 바 생성
sb = st.sidebar

if Auth.authenticate_token(Auth.load_token()):
    st.session_state['login'] = True
else:
    st.session_state['login'] = False

# 사이드바에서 선택상자를 메뉴로 사용
options = []
if st.session_state.login == True:
    options.append('할일')
    options.append('로그아웃')

else:
    options.append('로그인')
    options.append('사용자 등록')
    options.append('비밀번호 초기화')

menu = sb.selectbox('메뉴', options, key='menu_key')

if menu == '할일' and st.session_state.login == True:

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

elif menu == '로그인':

    st.subheader('로그인')
    with st.form(key='login_form'):

        user_email = st.text_input('이메일')
        user_pw = st.text_input('비밀번호', type='password')

        btn_login = st.form_submit_button('로그인')

        if btn_login:
            idToken = Auth.login_user(user_email, user_pw)
            if idToken is not None:
                Auth.store_session(idToken)
                st.session_state['login'] = True
                menu = '할일'
                st.experimental_rerun()
            else:
                st.error('아이디, 비밀번호를 확인 후 다시 로그인하세요.')


elif menu == '사용자 등록':

    st.subheader('사용자 등록')
    with st.form(key='user_reg_form'):

        user_name = st.text_input('이름')
        user_email = st.text_input('이메일')
        user_pw = st.text_input('비밀번호', type='password')

        btn_user_reg = st.form_submit_button('사용자 등록')

        if btn_user_reg:
            res = None
            res = Auth.create_user(user_name, user_email, user_pw)
            if res is None:
                st.info('사용자가 등록되었습니다.')
            else:
                st.error(res)

elif menu == '로그아웃':

    st.info('로그 아웃 하려면 로그아웃 버튼을 클릭하세요.')
    btn_logout = st.button('로그아웃')
    if btn_logout:
        Auth.revoke_token(Auth.load_token())
        st.experimental_rerun()

elif menu == '비밀번호 초기화':

    st.subheader('비밀번호 초기화')

    with st.form(key='pw_reset_form'):

        user_email = st.text_input('이메일')

        btn_reset = st.form_submit_button('비밀번호 초기화 메일 발송')

        if btn_reset:

            if Auth.reset_password(user_email):
                st.info('이메일을 확인하세요.')
            else:
                st.error('이메일이 정확한지 확인하세요!')