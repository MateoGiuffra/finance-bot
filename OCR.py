import re 
import pytesseract
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv() 

pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD", "tesseract")

    
def get_the_ticket_total(img_path: str):
    try:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
        
        pattern = r'TOTAL.*?([\d]+[.,]\d{2})'
        match = re.findall(pattern, text, re.IGNORECASE)
        
        if match:
            return match[-1]
        else:
            return None
    except Exception as e:
        print(f"Error processing image: {e}")
        raise RuntimeError("Error processing image") from e