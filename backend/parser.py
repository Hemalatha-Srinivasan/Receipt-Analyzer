import pytesseract
from PIL import Image
import re

# Specify the path to the Tesseract OCR executable.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Extracts text content from an image using OCR.
def extract_text_from_image(image_path, lang='eng'):

    # Open the image and apply OCR using the specified language.
    return pytesseract.image_to_string(Image.open(image_path), lang=lang)

# Parses the extracted text and retrieves receipt fields.
def extract_fields(text):

    vendor = "Unknown"    # Default vendor name
    date = "Unknown"      # Default date value
    amount = 0.0          # Default amount value
    currency = "₹"        # Default currency (INR)

    # Extract total amount from text (e.g., TOTAL: 123.45)
    total_match = re.search(r"TOTAL\s*[:=]?\s*(\d+[.,]?\d*)", text, re.IGNORECASE)
    
    if total_match:
        amount = float(total_match.group(1))

    # Detect currency symbol (₹, $, €, or Rs.)
    currency_match = re.search(r'(?i)(₹|\$|€|Rs\.?)', text)
    
    if currency_match:
        currency = currency_match.group(1)

    # Extract date in standard dd/mm/yyyy or dd-mm-yyyy format
    date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text)
   
    if date_match:
        date = date_match.group(1)

    # Assume vendor name is present in the first line of text
    lines = text.splitlines()
    
    if lines:
        vendor = lines[0].strip()

    # Return a dictionary with the extracted fields
    return {
        "vendor": vendor,
        "date": date,
        "amount": amount,
        "currency": currency
    }
