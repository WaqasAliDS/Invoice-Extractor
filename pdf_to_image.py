import fitz  # PyMuPDF
from PIL import Image

def pdf_to_image(pdf_files, dpi=300):
    pdf_images = []
    for pdf_file in pdf_files:
        pdf_bytes = pdf_file.read()  # Read the uploaded file as bytes
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        images = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            zoom = dpi / 72  # 72 is the default DPI of the PDF
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
            
        pdf_images.extend(images)
    return pdf_images



