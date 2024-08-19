import os
import sys
import time
import zipfile
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def upload_to_google_drive(file_path, credentials_path):
    # Authentification avec Google Drive
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    # Ajout d'un horodatage au nom du fichier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name_with_timestamp = f"{os.path.basename(file_path)}_{timestamp}.zip"
    file_metadata = {'name': file_name_with_timestamp}
    media = MediaFileUpload(file_path, mimetype='application/zip')

    # Upload du fichier sur Google Drive
    file = service.files().cr
