import os
import pickle
import time
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import email

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def mark_as_read(message_id):
    service = authenticate()
    service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()

def get_email_content(message_id):
    service = authenticate()
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    msg_str = base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data']).decode('utf-8')
    msg = email.message_from_string(msg_str)
    print('From:', msg['From'])
    print('Subject:', msg['Subject'])
    print('Message:', msg.get_payload())

def check_and_process_unread_emails():
    service = authenticate()
    results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
    messages = results.get('messages', [])

    if messages:
        for message in messages:
            message_id = message['id']
            get_email_content(message_id)
            mark_as_read(message_id)

if __name__ == '__main__':
    while True:
        check_and_process_unread_emails()
        time.sleep(5)
