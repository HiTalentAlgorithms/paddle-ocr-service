import base64
import datetime
import os

import requests


def test_ocr():
    f = open("image_1.png", "rb")
    print(datetime.datetime.now().isoformat())
    response = requests.post("http://192.168.8.191:5000/image2pdf", files={"file": f.read()})
    print(response.content)
    print(datetime.datetime.now().isoformat())
    with open("asdd.pdf", "wb") as file:
        file.write(response.content)


def test_face(path, filename):
    f = open(path, "rb")
    print(f"--------------{filename}----------------")
    print(datetime.datetime.now().isoformat())
    response = requests.post("http://192.168.8.191:5000/faceImages", files={"file": f.read()})
    if response.status_code != 200:
        print(f"code:{response.status_code} not a pdf {filename}")
        os.makedirs(f"out_image/{filename}-not-pdf")
        return
    # print(response.content)
    print(datetime.datetime.now().isoformat())
    images = response.json()['images']
    i = 0
    os.makedirs(f"out_image/{filename}")
    for image in images:
        i += 1
        with open(f"out_image/{filename}/imaeg_{str(i)}.png", "wb") as file:
            b = base64.b64decode(image)
            file.write(b)
    print("-------------------END-------------------")


test_ocr()
# dir_path = "English Resumes (Uncategorized)"
# for filename in os.listdir(dir_path):
#     test_face(os.path.join(dir_path, filename), filename)
