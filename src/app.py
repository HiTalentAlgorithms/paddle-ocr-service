import base64
import os
import uuid

import magic
from flask import Flask, request, jsonify
from werkzeug.exceptions import abort

from lib.face import check_face
from lib.ocr import image_to_pdf
from lib.pdf_process import pdf_to_image, ext_pdf_images
from lib.util import delete_dir
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
    with open(image_path, "rb") as file:
        buffer = file.read()
    os.remove(image_path)
    return buffer


@app.route('/faceImages', methods=['POST'])
def get_face_images():
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
    image_dir = ext_pdf_images(file_path)
    images = []
    for image_path in os.listdir(image_dir):
        abs_path = os.path.join(image_dir, image_path)
        if check_face(abs_path):
            with open(abs_path, "rb") as file:
                images.append(base64.b64encode(file.read()).decode())
    delete_dir(image_dir)
    return jsonify({"images": images})


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
