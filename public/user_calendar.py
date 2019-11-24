from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pprint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate_user(email='mail.com'):
    creds = None
    path_user_token = '../calendar_cache/token.' + email + '.pickle'
    path_credentials = '../credentials.json'
    if os.path.exists(path_user_token):
        with open(path_user_token, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path_credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(path_user_token, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_calendar_id_and_timezone(service):
    calendar_list = service.calendarList().list().execute()
    calendar_id = calendar_list['items'][0]['id']  # get the id of the calendar
    time_zone = calendar_list['items'][0]['timeZone']
    return calendar_id, time_zone

def add_event_to_calendar(service=None, calendar_id=None, title='Default', location='Georgia Tech', description='',
                          formatted_start='2019-11-28T09:00:00-07:00', formatted_end='2019-11-28T17:00:00-07:00',
                          time_zone='America/New_York'):
    if calendar_id is None or service is None:
        return None

    # add new events
    event = {
        'summary': title,
        'location': location,
        'description': description,
        'start': {
            'dateTime': formatted_start,
            'timeZone': time_zone,
        },
        'end': {
            'dateTime': formatted_end,
            'timeZone': time_zone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 15},
            ],
        },
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return event
