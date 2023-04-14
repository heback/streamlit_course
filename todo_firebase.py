import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from enum import Enum
from datetime import datetime

class User(Enum):
    user_name = u'user_name'
    user_gender = u'user_gender'
    user_id = u'user_id'
    user_pw = u'user_pw'
    user_email = u'user_email'
    user_mobile = u'user_mobile'
    reg_date = u'reg_date'

# Setup
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def getUsers():

    docs = db.collection(u'users').get()  # .stream()
    return docs


def getUser(name: str):
    docs = db.collection(u'users').order_by('reg_date').limit(3).get()
    return docs


def addUser(user: dict):
    ref = db.collection(u'users').document()
    ref.set(user)


# users = getUsers()
# for user in users:
#     print(user.id, '=>', user.to_dict(), end='\n')

users = getUser('홍길동')
for user in users:
    print(user.id, '=>', user.to_dict(), end='\n')

data = {
    u'user_name': u'홍길동',
    u'user_gender': u'남',
    u'user_id': u'heback9',
    u'user_pw': u'1111',
    u'user_email': u'heback9@gmail.com',
    u'user_mobile': u'010-9807-6103',
    u'reg_date': str(datetime.now())
}
addUser(data)