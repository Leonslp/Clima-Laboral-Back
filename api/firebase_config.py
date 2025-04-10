# api/firebase_config.py
import firebase_admin
from firebase_admin import credentials, storage

# Solo inicializamos una vez
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_credentials.json")  # <- reemplaza esto
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'clio7f.appspot.com'  # <- reemplaza esto también
    })
    
bucket = storage.bucket()
