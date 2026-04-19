import sys
import os
from googleapiclient.http import MediaFileUpload
from google_service_auth import get_service

def upload_to_drive(file_path, parent_folder_id):
    """Uploads a file to Google Drive and returns its web view link."""
    service = get_service('drive', 'v3')

    filename = os.path.basename(file_path)
    file_metadata = {
        'name': filename,
        'parents': [parent_folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    print(f"File uploaded: {filename}")
    print(f"File ID: {file.get('id')}")
    print(f"Link: {file.get('webViewLink')}")
    
    return file.get('webViewLink')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python upload_to_drive.py <file_path> <parent_folder_id>")
        sys.exit(1)

    file_path = sys.argv[1]
    parent_folder_id = sys.argv[2]
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    upload_to_drive(file_path, parent_folder_id)
