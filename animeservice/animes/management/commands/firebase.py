from config.settings import FIREBASE_CONFIG
import firebase_admin
from firebase_admin import firestore, credentials

# Remember the code we copied from Firebase.
#This can be copied by clicking on the settings icon > project settings, then scroll down in your firebase dashboard
config={
    "apiKey": FIREBASE_CONFIG["API_KEY"],
    "authDomain": FIREBASE_CONFIG["AUTH_DOMAIN"],
    "databaseURL": FIREBASE_CONFIG["DATABASE_URL"],
    "projectId": FIREBASE_CONFIG["PROJECT_ID"],
    "storageBucket": FIREBASE_CONFIG["STORAGE_BUCKET"],
    "messagingSenderId": FIREBASE_CONFIG["MESSAGING_SENDER_ID"],
    "appId": FIREBASE_CONFIG["APP_ID"],
    "measurementId": FIREBASE_CONFIG["MEASUREMENT_ID"]
}

cred = credentials.Certificate('serviceAccountKey.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
