from PIL import Image
import pytesseract

# Load the CAPTCHA image (replace 'captcha.png' with your image file)
image_path = 'captcha.png'
image = Image.open(image_path)

# Perform OCR and extract text
captcha_text = pytesseract.image_to_string(image)

# Print the recognized text
print(f"Captcha text: {captcha_text}")
