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

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../../calendar_cache/token.pickle'):
        with open('../../calendar_cache/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../../calendar_cache/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # List all the calenders
    calendar_list = service.calendarList().list().execute()
    calendar_id = calendar_list['items'][0]['id']  # get the id of the calendar
    time_zone = calendar_list['items'][0]['timeZone']

    # get all events
    # events = service.events().list(calendarId=calendar_id).execute()
    # pprint.pprint(len(events['items'])) # all calender events

    # add new events
    # event = {
    #     'summary': 'Google I/O 2015',
    #     'location': '800 Howard St., San Francisco, CA 94103',
    #     'description': 'A chance to hear more about Google\'s developer products.',
    #     'start': {
    #         'dateTime': '2019-11-28T09:00:00-07:00',
    #         'timeZone': time_zone,
    #     },
    #     'end': {
    #         'dateTime': '2019-11-28T17:00:00-07:00',
    #         'timeZone': time_zone,
    #     },
    #     'reminders': {
    #         'useDefault': False,
    #         'overrides': [
    #             {'method': 'email', 'minutes': 24 * 60},
    #             {'method': 'popup', 'minutes': 15},
    #         ],
    #     },
    # }
    #
    # event = service.events().insert(calendarId=calendar_id, body=event).execute()
    # print('Event created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    main()
