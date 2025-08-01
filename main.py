from flask import Flask, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

app = Flask(__name__)

@app.route('/get-events', methods=['GET'])
def get_events():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    # Load credentials from environment variable
    credentials_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    creds = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES
    )

    # Build Google Calendar service
    service = build('calendar', 'v3', credentials=creds)
    events_result = service.events().list(
        calendarId='primary', maxResults=5, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return jsonify(events)

# Only needed for local testing
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
