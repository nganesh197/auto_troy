from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

import os, json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']

def get_creds():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service 

def call_Gmail(service):
    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
    
def create_text_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}
            
def create_message_with_attachment(
    sender, to, subject, message_text, file):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(file, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}   

def send_message(service, user_id, message):

    message = (service.users().messages().send(userId=user_id, body=message).execute())
    print('Message Id: %s' % message['id'])
    return message

def send_error_message(email_address, message):
  error_subject = '[ERROR] Auto Troy!'
  get_service = get_creds()
  error_develop_message = create_text_message(email_address, email_address, error_subject, message)
  error_out_of_here = send_message(get_service, user_id='me', message=error_develop_message)

def filter_monitor(query="[RUN AUTO TROY]"):
  get_service = get_creds()
  results = get_service.users().messages().list(userId='me', pageToken=1, q=query).execute()
  list_of_queried_messages = results["messages"]
  
  #currently guessing that first list item is the most recent email message
  message_id = list_of_queried_messages[0]['id']
  filtered_message = get_service.users().messages().get(userId='me', id=message_id).execute()
  date_of_message = filtered_message['payload']['headers'][6]['value']
  subject_line = filtered_message['payload']['headers'][7]['value']
  
  #sanity check
  if subject_line == '[RUN AUTO TROY]':
    with open("logged_runs.json", 'r') as logged_runs:
      logged = json.load(logged_runs)
    if logged['ids_count']< len(list_of_queried_messages):
      count_of_ids = len(list_of_queried_messages)
      update_count = {}
      update_count['ids_count'] = count_of_ids
      with open("logged_runs.json", 'w') as update_log:
        json.dump(update_count, update_log)
      return True
         

def send_day_pass(filepaths, email_address, to_watch):
    phone_filepath, watch_filepath = filepaths
    get_service = get_creds()
    phone_develop_message = create_message_with_attachment(email_address, email_address, '[PHONE] TROJANCHECK QR SCREENSHOT', 'Screenshot of QR Code taken by Automate TrojanCheck. Person has complied with USC policies and is using this program to obtain QR code.\n', phone_filepath)
    watch_develop_message = create_message_with_attachment(email_address, email_address, '[WATCH] TROJANCHECK QR SCREENSHOT', 'Screenshot of QR Code taken by Automate TrojanCheck. Person has complied with USC policies and is using this program to obtain QR code.\n', watch_filepath)
    phone_get_out_of_here = send_message(get_service, user_id='me', message=phone_develop_message)
    if to_watch:
      watch_get_out_of_here = send_message(get_service, user_id='me', message=watch_develop_message)
      
      
# if __name__ == '__main__':
#     print(filter_monitor())