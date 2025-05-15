from oauth2client.service_account import ServiceAccountCredentials
from tickets.app_config import GOOGLE_SHEETS_CREDENTIALS
import gspread
import json

credentials = json.loads(GOOGLE_SHEETS_CREDENTIALS)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(creds)

spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1G4BY0wblwZCedVkE3GbqNTOEae5FN6qMGPk4jjd7i-M/edit?gid=0#gid=0")
worksheet = spreadsheet.sheet1
