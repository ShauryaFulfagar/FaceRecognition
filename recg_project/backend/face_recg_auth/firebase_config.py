import firebase_admin
from firebase_admin import credentials, firestore

# Path to your Firebase service account key
cred = credentials.Certificate('face_recg_auth/facerecognition-7a16b-firebase-adminsdk-s62vc-a9902d4933.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
