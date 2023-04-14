import pyrebase

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

#Update data with known path
db.child("todolistA").child("monday").child("paper").update({"deadline":"1pm"})

#Multi-location update data
data={"todolistA/monday/paper":{"details":"v2"}, "todolistA/tuesday/filmvideo":{"deadline":"7pm"}}
db.update(data)

#Update data with unknown key
monday_tasks=db.child("todolistB").child("monday").get()
for task in monday_tasks.each():
    if(task.val()['name']=="paper"):
        key=task.key()
db.child("todolistB").child("monday").child(key).update({"deadline":"1pm"})