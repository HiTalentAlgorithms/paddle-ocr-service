import os
import uuid

import magic
from flask import Flask, request
from werkzeug.exceptions import abort

from lib.ocr import image_to_pdf
from lib.pdf_process import pdf_to_image
from lib.util import save_file
from settings import TEMPDIR

app = Flask(__name__)

mime = magic.Magic(mime=True)


@app.route('/')
def hello_world():
    # Check the health
    return 'Hello World'


@app.route('/image2pdf', methods=['POST'])
def image2pdf():
    """
    图片ocr 转为pdf文件
    :return: pdf文件内容
    """
    upload_file = request.files['file']
    file_name = str(uuid.uuid4())
    file_path = os.path.join(TEMPDIR, file_name)
    upload_file.save(file_path)
    file_type = mime.from_file(file_path)
    if file_type == "application/pdf":
        file_path = pdf_to_image(file_path)
    elif "image" not in file_type:
        abort(400, 'Must be a image')
    error, content = image_to_pdf(file_path)
    if error:
        abort(500, error)
    return content


@app.route('/pdf2image', methods=['POST'])
def pdf2image():
    """
    将pdf 转为单个长图片
    :return: 图片字节内容
    """
    upload_file = request.files['file']
    file_name = str(uuid.uuid4())
    file_path = os.path.join(TEMPDIR, file_name)
    upload_file.save(file_path)
    file_type = mime.from_file(file_path)
    if file_type != "application/pdf":
        abort(400, 'Must be a pdf')
    image_path = pdf_to_image(file_path)
    with open(image_path,"rb") as file:
        buffer = file.read()
    os.remove(image_path)
    return buffer


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
