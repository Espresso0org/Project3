from PIL import Image
import requests
import pytesseract
from io import BytesIO

# Replace 'your_image_url_here' with the actual image URL
image_url = 'your_image_url_here'

# Download the image from the URL
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

# Perform OCR and extract text
text = pytesseract.image_to_string(image)

# Print the recognized text
print(text)
