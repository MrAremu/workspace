import sys
import base64
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google_service_auth import get_service

def send_gmail(to, subject, body_text, attachment_path=None):
    """Sends an email using the Gmail API."""
    service = get_service('gmail', 'v1')

    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject

    msg = MIMEText(body_text)
    message.attach(msg)

    if attachment_path and os.path.exists(attachment_path):
        content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        
        with open(attachment_path, 'rb') as fp:
            file_data = fp.read()
        
        filename = os.path.basename(attachment_path)
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(file_data)
        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    body = {'raw': raw_message}

    try:
        message_response = service.users().messages().send(userId='me', body=body).execute()
        print(f"Message sent. ID: {message_response['id']}")
        return message_response
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # Usage: py send_gmail.py <to> <subject> <body> [attachment_path]
    if len(sys.argv) < 4:
        print("Usage: python send_gmail.py <to> <subject> <body> [attachment_path]")
        sys.exit(1)

    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachment_path = sys.argv[4] if len(sys.argv) > 4 else None

    send_gmail(to, subject, body, attachment_path)
