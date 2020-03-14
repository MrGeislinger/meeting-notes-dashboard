from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_service():
    '''
    Use credentials to authorize service.
    '''
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('secrets/token.pickle'):
        with open('secrets/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secrets/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('secrets/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def get_one_on_one_events(start_time, max_results=10):
    '''
    '''
    service = get_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(
                                        calendarId='primary', timeMin=now,
                                        maxResults=max_results, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')


    # Only get "1 on 1" events based on event summary (name of event)
    one_on_one_str = '1 on 1'
    one_on_one_events = [event for event in events
                                    if one_on_one_str in event['summary']]

    return one_on_one_events


def get_current_one_on_one(one_on_one_events):
    '''
    '''
    #
    return one_on_one_events[0]
