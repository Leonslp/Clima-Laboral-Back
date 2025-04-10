import firebase_admin
from firebase_admin import credentials, storage
from decouple import config

firebase_config = {
    "type": config('FB_TYPE'),
    "project_id": config('FB_PROJECT_ID'),
    "private_key_id": config('FB_PRIVATE_KEY_ID'),
    "private_key": config('FB_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": config('FB_CLIENT_EMAIL'),
    "client_id": config('FB_CLIENT_ID'),
    "auth_uri": config('FB_AUTH_URI'),
    "token_uri": config('FB_TOKEN_URI'),
    "auth_provider_x509_cert_url": config('FB_AUTH_PROVIDER'),
    "client_x509_cert_url": config('FB_CLIENT_CERT')
}

cred = credentials.Certificate(firebase_config)

# Inicializar Firebase solo una vez
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'storageBucket': config('FB_STORAGE_BUCKET')
    })

# Este bucket lo usas desde cualquier vista
bucket = storage.bucket()
