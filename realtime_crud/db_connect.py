import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dataclasses import dataclass
from datetime import datetime

# Fetch the service account key JSON file contents
cred = credentials.Certificate('serviceAccount.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://flet-firebase-ced4d-default-rtdb.firebaseio.com/'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference()

@dataclass
class User:
    id: str
    name: str
    date_of_birth: str
    reg_date: str

    def to_json(self):
        return {
            self.id:{
                "name": self.name,
                "date_of_birth": self.date_of_birth,
                "reg_date": self.reg_date
            }
        }

    def to_sub_json(self):
        return {
                "name": self.name,
                "date_of_birth": self.date_of_birth,
                "reg_date": self.reg_date
            }



user_ref = ref.child('users')
u1 = User('heback', '이준구', '1972-03-25', str(datetime.now()))
u2 = User('heback5', '장은진', '1977-05-25', str(datetime.now()))
u3 = User('heback2', '이나영', '2003-12-25', str(datetime.now()))
u4 = User('heback1', '홍길동', '1982-07-25', str(datetime.now()))
u5 = User('heback3', '이도현', '2005-12-18', str(datetime.now()))

user_ref.child(u1.id).set(u1.to_sub_json())
user_ref.child(u2.id).set(u2.to_sub_json())
user_ref.child(u3.id).set(u3.to_sub_json())
user_ref.child(u4.id).set(u4.to_sub_json())
user_ref.child(u5.id).set(u5.to_sub_json())

user_ref.child(u3.id).update({
    'name': 'ddonggae Kim'
})

# snapshot = user_ref.order_by_child('reg_date').get()
# for key, val in snapshot.items():
#     print(f'{key}: {val}')

snapshot = user_ref.order_by_child('date_of_birth').limit_to_first(2).get()
for key, val in snapshot.items():
    print(f'{key}: {val}')