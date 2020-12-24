import os

TEMPDIR = os.environ.get('TEMPDIR', 'tmp')
TESSERACT_CMD = os.environ.get('TESSERACT_CMD', r"C:\Program Files\Tesseract-OCR\tesseract")