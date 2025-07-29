from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_calendar_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = 'watcherreminderbot-021b9e58a2fe.json'  # cambia el nombre si lo tuyo es distinto

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)
    return service
