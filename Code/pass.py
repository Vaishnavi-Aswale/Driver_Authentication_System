from firebase import firebase

fbLink="https://proj-db-c86ba.firebaseio.com"
#try:
refrence=firebase.FirebaseApplication(fbLink, None)
link='/LMV/9983'
data={
    'Pass':1234567
    }
refrence.post(link,data)