from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'steady-velocity-454513-t0-9ba8ec419e7d.json'
PARENT_FOLDER_ID = "1slvU_jG7aFuXnz07dvJ_PDVMlch45tne"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def create_subfolder(folder_name):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name' : folder_name,
        'mimeType' : 'application/vnd.google-apps.folder',
        'parents' : [PARENT_FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata
    ).execute()

    return file.get('id')

def upload_file(file_name, folder_id):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name' : file_name,
        'parents' : [folder_id]
    }

    media = MediaFileUpload(file_name, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media
    ).execute()

    return file.get('id')

# file_id = upload_file("test.txt", "1jShcYbt1mKYbEbkFiREyY_cF5noVEwKt")
# print(file_id)

# folder_id = create_subfolder("Test-Folder-1")
# print(folder_id)