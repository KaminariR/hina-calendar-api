from flask import Flask, jsonify, request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timezone
import os
import json
from dotenv import load_dotenv

# Încarcă variabilele din .env
load_dotenv()

app = Flask(__name__)

@app.route('/get-events', methods=['GET'])
def get_events():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    credentials_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    creds = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES
    )

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.now(timezone.utc).isoformat()
    calendar_id = request.args.get('calendarId', 'primary')

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=5,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    return jsonify(events)

@app.route('/get-calendars', methods=['GET'])
def get_calendars():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    credentials_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    creds = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES
    )

    service = build('calendar', 'v3', credentials=creds)

    calendar_list = service.calendarList().list().execute()
    return jsonify(calendar_list.get('items', []))

# Punctul de pornire pentru Render
def start():
    app.run(host='0.0.0.0', port=8080)

start()
