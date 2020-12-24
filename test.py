import datetime

import requests

f = open("test.png", "rb")
print(datetime.datetime.now().isoformat())
response = requests.post("http://192.168.8.191:5000/image2pdf", files={"file": f.read()})
print(datetime.datetime.now().isoformat())
print(response.content)
with open("out.pdf","wb") as file:
    file.write(response.content)
