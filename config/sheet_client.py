from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from decouple import config
import gspread
import json

load_dotenv() 
GOOGLE_SHEETS_CREDENTIALS = config("GOOGLE_SHEETS_CREDENTIALS")
credentials = json.loads(GOOGLE_SHEETS_CREDENTIALS)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(creds)

spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1G4BY0wblwZCedVkE3GbqNTOEae5FN6qMGPk4jjd7i-M/edit?gid=0#gid=0")
worksheet = spreadsheet.sheet1
