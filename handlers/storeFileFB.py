import os
import datetime
import firebase_admin
from firebase_admin import credentials, storage

class FirebaseStorageHandler:
    def __init__(self):
        cred_path = '/home/if22b009/projects/Smart Home Monitoring/handlers/serviceAccountKey.json'
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'smart-home-monitoring-f043a.appspot.com'
        })
        self.bucket = storage.bucket()

    def store_file(self, file_path):
        now = datetime.datetime.now()
        timestamp = now.strftime("%d.%m.%Y-%H:%M")

        original_filename = os.path.basename(file_path)
        filename = f"Motion_{timestamp}"
        extension = os.path.splitext(original_filename)[1]
        full_filename = filename + extension
        
        blob = self.bucket.blob(full_filename)
        blob.upload_from_filename(file_path)
        blob.make_public()
        print(f"File {full_filename} uploaded to Firebase Storage.")
        return blob.public_url
