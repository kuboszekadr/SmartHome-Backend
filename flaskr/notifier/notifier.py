import base64
import os
import pickle

from flask import Blueprint, request

# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# for dealing with attachement MIME types
from email.mime.text import MIMEText

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
PATH = os.path.dirname(os.path.abspath(__file__))

bp = Blueprint('notifier', __name__)


@bp.route("/notifier", methods=["POST"])
def notify():
    data = request.get_json()

    try:
        send_email(data["title"], data["message"])
    except Exception as err:
        return str(err), 500

    return 'OK', 200


def send_email(title: str, message: str):
    service = gmail_authenticate()
    receivers = os.environ["RECEIVERS"]

    message = create_message('me', receivers, title, message)
    send_message(service=service, user_id='me', message=message)


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    token_file = os.path.join(PATH, "token.pickle")
    credentials_file = os.path.join(PATH, "credentials.json")

    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open(token_file, "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(error)
