import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
# Fetch the service account key JSON file contents
cred = credentials.Certificate('test-f3464-firebase-adminsdk-rkob1-05d762f90b.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
     'databaseURL': 'https://test-f3464-default-rtdb.asia-southeast1.firebasedatabase.app',
    # 'databaseURL' : "http://127.0.0.1:9000/?ns=test-f3464-default-rtdb",
})

db = firestore.client()

# Add a new doc in collection 'cities' with ID 'LA'
ref = db.collection('server/tennis_app/scores')
data_red = ref.document('sets_data')
with open('Matches_until_may20.json', 'r') as f:
    data = json.load(f)
    del data['schema']['fields'][1]
    key_value ={}
    for i in data['data']:
        gameID = i['GameID']
        del i['GameID']
        key_value[gameID] = i 
    data_red.set(key_value)

schema_red = ref.document('schema')
with open('Matches_until_may20.json', 'r') as f:
    data = json.load(f)
    del data['data']
    