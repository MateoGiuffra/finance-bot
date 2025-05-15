import re 
import pytesseract
from PIL import Image
from tickets.app_config import CMD_DIR

pytesseract.pytesseract.tesseract_cmd = CMD_DIR 

    
def get_the_ticket_total(img_path: str):
    try:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img, config='--psm 6')
        
        pattern = r'TOTAL.*?([\d]+[.,]\d{2})'
        match = re.findall(pattern, text, re.IGNORECASE)
        
        if match:
            return match[-1]
        else:
            return None
    except Exception as e:
        print(f"Error processing image: {e}")
        # raise RuntimeError("Error processing image") from e

# print(get_the_ticket_total("tickets/asd.jpg"))