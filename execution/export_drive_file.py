import sys
import os
import io
from googleapiclient.http import MediaIoBaseDownload
from google_service_auth import get_service

def export_drive_file(file_id, mime_type='application/pdf'):
    """Exports a Google Drive file to a given MIME type and saves it locally."""
    service = get_service('drive', 'v3')
    
    # Get file metadata to get name
    file_metadata = service.files().get(fileId=file_id).execute()
    filename = file_metadata.get('name', 'exported_file')
    
    # Clean filename
    safe_filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c in (' ', '-', '_')]).rstrip()
    if mime_type == 'application/pdf':
        safe_filename += '.pdf'
    
    output_path = os.path.join('.tmp', safe_filename)

    request = service.files().export_media(fileId=file_id, mimeType=mime_type)
    
    with io.FileIO(output_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            # print(f"Download {int(status.progress() * 100)}%.")

    print(f"File exported to: {output_path}")
    return output_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python export_drive_file.py <file_id> [mime_type]")
        sys.exit(1)

    file_id = sys.argv[1]
    mime_type = sys.argv[2] if len(sys.argv) > 2 else 'application/pdf'
    
    export_drive_file(file_id, mime_type)
