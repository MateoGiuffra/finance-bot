from dotenv import load_dotenv
from decouple import config
import os 
load_dotenv() 

CMD_DIR = os.getenv("TESSERACT_CMD", "tesseract")
GOOGLE_SHEETS_CREDENTIALS = config("GOOGLE_SHEETS_CREDENTIALS")
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Check if the environment variables are set
IS_NOT_MESSAGE = "is not set in the environment variables."

if TOKEN is None:
    raise ValueError("TESSERACT_CMD" + IS_NOT_MESSAGE)
if GOOGLE_SHEETS_CREDENTIALS is None:
    raise ValueError("TESSERACT_CMD" + IS_NOT_MESSAGE)
if CMD_DIR is None:
    raise ValueError("TESSERACT_CMD" + IS_NOT_MESSAGE)