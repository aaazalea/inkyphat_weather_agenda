import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dateutil.parser import parse
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_events():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # hack to get events from today but not last night. Day ends at 4am.
    now = datetime.datetime.now()
    now -= datetime.timedelta(hours=4)
    now_str = now.replace(hour=8, minute=0, second=0, microsecond=0).isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting data from google calendar...')
    # Call the Calendar API
    events_result = service.events().list(calendarId='primary', timeMin=now_str,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    # return events
    results = []
    for event in events:
        start = event['start'].get('dateTime', None)
        start_dt = None
        fmt = ''
        if start is None:
            # all day
            start_date = event['start'].get('date')
            start_dt = datetime.datetime.strptime(start_date, r'%Y-%m-%d')
        else:
            start_dt = parse(start)
            fmt = start_dt.strftime("%H:%M") if start_dt.minute else start_dt.strftime("%H")
            
        # results.append((fmt, start_dt.date(), event['summary']))   
        if start_dt.date() <= datetime.datetime.now().date():
            results.append((fmt,event['summary']))
    
    if len(results) == 0:
        return [('', "Nothing on the agenda")]
    else:
        return results
# [
#     ('','Ltchin in town'), # all day event
#     ('11','brunch w ava'),
#     ('13','crossword cousins'),
#     ('20:45','call parentsa'),
#     ('21','Chores'),
# ]
if __name__ == '__main__':
    print(get_events())