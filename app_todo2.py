import streamlit as st
import datetime
from todo import TodoDB
# pip install email-validator
from email_validator import validate_email, EmailNotValidError
import re

db = TodoDB()
db.connectToDatabase()

sb = st.sidebar
menu = sb.selectbox('메뉴', ['회원가입', '할일', '통계'], index=0, key='mnu')

if menu == '회원가입':
    ucol1, ucol2 = st.columns(2)

    with ucol1:
        st.subheader('회원가입')

    with ucol2:
        st.subheader('회원목록')


elif menu == '할일':
    pass

elif menu == '통계':
    pass