import base64
import json
import time

import requests

with open("test/a.png", "rb") as f:
    content = f.read()
data = {"images": [base64.b64encode(content).decode('utf8')]}

while 1:
    # print(data)
    response = requests.post("http://127.0.0.1:8866/predict/ocr_system",
                             headers={"Content-type": "application/json"},
                             data=json.dumps(data))
    print(response.elapsed, response.json())
