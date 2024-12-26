import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
import json
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

# Fetch the service account key JSON file contents
cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_KEY'))

# Set the FIREBASE_EMULATOR_HOST environment variable to publish to emulator
# os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"

# Initialize the app with a service account, granting admin privileges
print(os.environ.get('FIRESTORE_EMULATOR_HOST'))

default_app = firebase_admin.initialize_app(cred, {
     'databaseURL': 'https://test-f3464-default-rtdb.asia-southeast1.firebasedatabase.app',
})

app = firebase_admin.get_app()
store = firebase_admin.firestore.client()

# print(vars(app._services['_firestore']._client))
print('connecting to emulator host: ', app._services['_firestore']._client._emulator_host)
#print(vars(app._services['_firestore']._client._credentials))
if app._services['_firestore']._client._emulator_host !=  '127.0.0.1:8080': 
	print('Emulator disconnected')
	ref = store.collection('scores')
	data_red = ref.document('sets_data')

	with open('./data/Matches_until_may20.json', 'r') as f:
		data = json.load(f)
		del data['schema']['fields'][1]
		key_value = {}
		for i in data['data']:
			i['Date'] = datetime.datetime.fromisoformat(i['Date'])
			gameID = i['GameID']
			del i['GameID']
			key_value[gameID] = i 
			data_red.set(key_value)
else: 
# Add a new doc in collection 'cities' with ID 'LA'
	ref = store.collection('scores')
	data_red = ref.document('sets_data')

	with open('./data/Matches_until_may20.json', 'r') as f:
		data = json.load(f)
		del data['schema']['fields'][1]
		key_value = {}
		for i in data['data']:
			i['Date'] = datetime.datetime.fromisoformat(i['Date'])
			gameID = i['GameID']
			del i['GameID']
			key_value[gameID] = i 
			data_red.set(key_value)
    
