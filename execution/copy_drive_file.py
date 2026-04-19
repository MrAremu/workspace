import sys
from google_service_auth import get_service

def copy_drive_file(file_id, destination_folder_id, new_name):
    """Copies a file in Google Drive and renames it."""
    service = get_service('drive', 'v3')

    body = {
        'name': new_name,
        'parents': [destination_folder_id]
    }

    try:
        drive_response = service.files().copy(
            fileId=file_id,
            body=body,
            fields='id,webViewLink'
        ).execute()
        
        print(f"File copied successfully. ID: {drive_response.get('id')}")
        print(f"Link: {drive_response.get('webViewLink')}")
        return drive_response
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python copy_drive_file.py <file_id> <destination_folder_id> <new_name>")
        sys.exit(1)

    file_id = sys.argv[1]
    dest_folder_id = sys.argv[2]
    new_name = sys.argv[3]
    
    copy_drive_file(file_id, dest_folder_id, new_name)
