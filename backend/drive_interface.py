
#IMPORTANT MAKE SURE YOU HAVE THIS
#pip install google-auth-oauthlib google-auth-httplib2 googleapiclient


from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
import os

# Define the scope for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

# Authenticate and get credentials
def authenticate():
    creds = None
    # Load credentials if they exist
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Authenticate user if credentials are invalid or don't exist
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret_160309272049-27l2ei9e1362anloj8vvlgf7scghqndp.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

# Function to create a folder in Google Drive
def create_folder(folder_name):
    service = authenticate()
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    print(f'✅ Folder "{folder_name}" created with ID: {folder["id"]}')
    return folder['id']

# Function to upload a file to Google Drive
def upload_file(file_path, folder_id=None):
    service = authenticate()
    file_name = os.path.basename(file_path)
    
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'📂 File "{file_name}" uploaded successfully with ID: {file["id"]}')
    return file['id']

