import base64
import json

import requests


def test_PaddleOCR(content):
    headers = {"Content-type": "application/json"}
    data = {"images": [base64.b64encode(content).decode('utf8')]}
    response = requests.post("http://127.0.0.1:8866/predict/ocr_system", headers=headers,
                             data=json.dumps(data))
    return response.json()


with open("image0.png", "rb") as f:
    json_data = test_PaddleOCR(f.read())
    print(json.dumps(json_data))
