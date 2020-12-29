import base64
import datetime

import requests


def test_ocr():
    f = open("0003.pdf", "rb")
    print(datetime.datetime.now().isoformat())
    response = requests.post("http://192.168.8.191:5000/image2pdf", files={"file": f.read()})
    print(response.content)
    print(datetime.datetime.now().isoformat())
    with open("asd.pdf", "wb") as file:
        file.write(response.content)


def test_face(path):
    f = open(path, "rb")
    print(datetime.datetime.now().isoformat())
    response = requests.post("http://192.168.8.191:5000/faceImages", files={"file": f.read()})
    print(response.content)
    print(datetime.datetime.now().isoformat())
    images = response.json()['images']
    i = 0
    for image in images:
        i += 1
        with open(f"imaeg_{str(i)}.png", "wb") as file:
            b = base64.b64decode(image)
            print(b)
            file.write(b)

test_face("0003.pdf")