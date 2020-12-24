import json
import os
import uuid
from datetime import datetime

import magic
from flask import Flask, request, jsonify, Response
from werkzeug.exceptions import abort

from service import image_to_pdf
from settings import TEMPDIR

app = Flask(__name__)

mime = magic.Magic(mime=True)


@app.route('/')
def hello_world():
    # Check the health
    return 'Hello World'


@app.route('/image2pdf', methods=['POST'])
def image2pdf():
    upload_file = request.files['file']
    file_name = str(uuid.uuid4())
    file_path = os.path.join(TEMPDIR, file_name)
    upload_file.save(file_path)
    file_type = mime.from_file(file_path)
    if "image" not in file_type:
        abort(400, 'Must be a image')

    error, content = image_to_pdf(file_path)
    if error:
        abort(500, error)
    return content


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
