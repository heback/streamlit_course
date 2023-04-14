import pyrebase

#Initialize Firebase
firebaseConfig={
    'apiKey': "AIzaSyDhCADzL0Pu6ljILrAiVckNs3BmXJqb-pU",
    'authDomain': "flet-firebase-ced4d.firebaseapp.com",
    'databaseURL': "https://flet-firebase-ced4d-default-rtdb.firebaseio.com",
    'projectId': "flet-firebase-ced4d",
    'storageBucket': "flet-firebase-ced4d.appspot.com",
    'messagingSenderId': "570468785109",
    'appId': "1:570468785109:web:008672c9c6e4e233007b5c"
}

firebase=pyrebase.initialize_app(firebaseConfig)

db=firebase.database()

#Push Data
data={"age":20, "address":["new york", "los angeles"]}
print(db.push(data)) #unique key is generated

#Create paths using child
#data={"name":"Jane", "age":20}
#db.child("Branch").child("Employees").push(data)

#Create your own key
data={"age":20, "address":["new york", "los angeles"]}
db.child("John").set(data)

#Create your own key + paths with child
data={"name":"John", "age":20, "address":["new york", "los angeles"]}
db.child("Branch").child("Employee").child("male employees").child("John's info").set(data)


