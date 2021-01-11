# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))

from io import BytesIO

import fitz

sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))

# import cv2
# import numpy as np
import time
from PIL import Image
# from ppocr.utils.utility import get_image_file_list
# from tools.infer.utility import draw_ocr, draw_boxes

import requests
import json
import base64


def cv2_to_base64(image):
    return base64.b64encode(image).decode('utf8')


def get_pdf_images(path):
    doc = fitz.open(path)
    images = []
    for page in doc:
        mat = fitz.Matrix(1.3, 1.3).preRotate(0)
        pix = page.getPixmap(matrix=mat, alpha=False)
        images.append(pix.getImageData())
    return images


def test_PaddleOCR(content):
    headers = {"Content-type": "application/json"}
    data = {"images": [base64.b64encode(content).decode('utf8')]}
    response = requests.post("http://192.168.5.192:8866/predict/ocr_system", headers=headers,
                             data=json.dumps(data))
    return response.content


def test_ocr(content):
    response = requests.post("http://192.168.5.192:5000/image2pdf", files={"file": content})
    return response.content


root_path = "testpdf"
result = open("result33.csv", "w", encoding="utf-8")
result.write("file_path,pdf_page,resolution,tesseract_time,paddle_time\n")
for file in os.listdir(root_path):
    path = os.path.join(root_path, file)
    if os.path.isfile(path):
        out_path = path + "_out"
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        images = get_pdf_images(path)
        for i, image in enumerate(images):
            out_image_path = os.path.join(out_path, f"image{i}.png")
            with open(out_image_path, "wb") as f:
                f.write(image)
            paddle_start = time.time()
            paddle_content = test_PaddleOCR(image)
            paddle_end = time.time()

            tess_start = time.time()
            tess_content = test_ocr(image)
            tess_end = time.time()
            out_json_file_path = os.path.join(out_path, f"pdf{i}.json")
            with open(out_json_file_path, "wb") as f:
                f.write(paddle_content)

            out_pdf_file_path = os.path.join(out_path, f"pdf{i}.pdf")
            with open(out_pdf_file_path, "wb") as f:
                f.write(tess_content)
            im = Image.open(BytesIO(image))

            result.write(
                f"{path},{out_image_path},{im.width}x{im.height},{tess_end - tess_start},{paddle_end - paddle_start}\n")
            result.flush()
result.close()
