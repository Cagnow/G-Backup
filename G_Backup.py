import os
import sys
import time
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_google_drive(file_path, credentials_path):
    # Authentification avec Google Drive
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    # Ajout d'un horodatage au nom du fichier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name_with_timestamp = f"{os.path.basename(file_path)}_{timestamp}"
    file_metadata = {'name': file_name_with_timestamp}
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')

    # Upload du fichier sur Google Drive
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File uploaded successfully! File ID: {file.get('id')}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_file> <path_to_credentials>")
        sys.exit(1)

    file_path = sys.argv[1]
    credentials_path = sys.argv[2]

    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(credentials_path):
        print(f"The credentials file {credentials_path} does not exist.")
        sys.exit(1)

    while True:
        upload_to_google_drive(file_path, credentials_path)
        print("Waiting for 30 minutes before the next backup...")
        time.sleep(1800)  # Attendre 30 minutes (1800 secondes)
