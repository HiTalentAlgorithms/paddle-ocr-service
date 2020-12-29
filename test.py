import datetime

import requests

f = open("0003.pdf", "rb")
print(datetime.datetime.now().isoformat())
response = requests.post("http://192.168.8.191:5000/image2pdf", files={"file": f.read()})
print(response.content)
print(datetime.datetime.now().isoformat())
with open("ou8i2t.pdf", "wb") as file:
    file.write(response.content)
