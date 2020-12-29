import datetime

import requests

f = open("0003.pdf", "rb")
print(datetime.datetime.now().isoformat())
response = requests.post("http://192.168.8.191:5000/pdf2image", files={"file": f.read()})
print(response.content)
print(datetime.datetime.now().isoformat())
with open("qw.png", "wb") as file:
    file.write(response.content)
