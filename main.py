from flask import Flask, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json
from datetime import datetime, timezone

app = Flask(__name__)

def get_calendar_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    credentials_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    creds = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=creds)

@app.route('/get-events', methods=['GET'])
def get_events():
    service = get_calendar_service()
    now = datetime.now(timezone.utc).isoformat()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=5,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    return jsonify(events)

@app.route('/get-calendars', methods=['GET'])
def get_calendars():
    service = get_calendar_service()
    calendar_list = service.calendarList().list().execute()
    return jsonify(calendar_list.get('items', []))
