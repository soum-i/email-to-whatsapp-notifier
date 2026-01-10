
import os
import sys
import base64
import email
from twilio.rest import Client
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
import time

load_dotenv() 

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CRED_FILE = 'credentials.json'    
LAST_ID_FILE = 'last_msg_id.txt'


TW_SID = os.getenv("TWILIO_SID")
TW_AUTH = os.getenv("TWILIO_AUTH")
WHATSAPP_FROM = os.getenv("WHATSAPP_FROM")  
WHATSAPP_TO = os.getenv("WHATSAPP_TO")      

def require_envs():
    missing = [k for k,v in (("TWILIO_SID",TW_SID),("TWILIO_AUTH",TW_AUTH),
                             ("WHATSAPP_FROM",WHATSAPP_FROM),("WHATSAPP_TO",WHATSAPP_TO)) if not v]
    if missing:
        print("Missing env vars:", ", ".join(missing))
        sys.exit(1)

def gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if not os.path.exists(CRED_FILE):
            print(f"Missing {CRED_FILE}. Place your OAuth client JSON in project folder.")
            sys.exit(1)
        flow = InstalledAppFlow.from_client_secrets_file(CRED_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as f:
            f.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_latest_message(service):
    res = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
    msgs = res.get('messages', [])
    if not msgs:
        return None
    msg_id = msgs[0]['id']
    msg = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
    raw = base64.urlsafe_b64decode(msg['raw'].encode())
    mime = email.message_from_bytes(raw)
    subject = mime.get('subject', '(no subject)')
    sender = mime.get('from', '(no sender)')
    return msg_id, subject, sender

def read_last_id():
    if not os.path.exists(LAST_ID_FILE):
        return None
    return open(LAST_ID_FILE).read().strip()

def write_last_id(mid):
    with open(LAST_ID_FILE, 'w') as f:
        f.write(mid)

def send_whatsapp(subject, sender):
    client = Client(TW_SID, TW_AUTH)
    body = f"📧 New Email\nFrom: {sender}\nSubject: {subject}"
    msg = client.messages.create(from_=WHATSAPP_FROM, to=WHATSAPP_TO, body=body)
    print("sent:", msg.sid)

def main():
    require_envs()
    svc = gmail_service()
    latest = get_latest_message(svc)
    if not latest:
        print("no emails")
        return
    msg_id, subject, sender = latest
    if msg_id == read_last_id():
        print("already sent")
        return
    send_whatsapp(subject, sender)
    write_last_id(msg_id)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(120)
    
