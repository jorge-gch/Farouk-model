from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image

def image_to_pdf(image_path, pdf_path):
    img = Image.open(image_path)
    width_px, height_px = img.size
    dpi = img.info['dpi']
    dpi_x, dpi_y = dpi
    width_pt = width_px * 72 / dpi_x
    height_pt = height_px * 72 / dpi_y
    c = canvas.Canvas(pdf_path, pagesize=(width_pt, height_pt))
    image = ImageReader(image_path)
    c.drawImage(image, 0, 0, width=width_pt, height=height_pt)
    c.showPage()
    c.save()
