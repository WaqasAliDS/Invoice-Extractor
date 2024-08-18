from PIL import Image
import pytesseract
import io
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
def image_to_text(images):
    img_bytes = io.BytesIO()
    images.save(img_bytes, format='PNG')  
    text = pytesseract.image_to_string(Image.open(img_bytes))
    return text