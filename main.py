from flask import Flask, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

@app.route('/get-events', methods=['GET'])
def get_events():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    SERVICE_ACCOUNT_FILE = 'credentials.json'

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=creds)
    events_result = service.events().list(
        calendarId='primary', maxResults=5, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return jsonify(events)

app.run(host='0.0.0.0', port=8080)
