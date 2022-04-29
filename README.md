## Clone 
```
git clone https://github.com/HiTalentAlgorithms/paddle-ocr-service.git
```


## [CPU]Build and run
```
docker build -t minghealtomni/paddle-ocr .
docker run -d -p 8866:8866 --name 'ocr-service' minghealtomni/paddle-ocr
```
## [GPU]Build and run
```
docker build -t minghealtomni/paddle-ocr-gpu -f Dockerfile_GPU .
docker run --name paddle-ocr-gpu -dp 8866:8866 --rm --gpus all  minghealtomni/paddle-ocr-gpu 
```

## API Url: /predict/ocr_system 
    Methods:
        Post: Extract text from PDF images using Paddle OCR
            Request: {"images": ["base64 of image"]}
            Response: image text json

python
```python
import base64
import json
import requests


with open("image0.png", "rb") as f:
    content = f.read()
data = {"images": [base64.b64encode(content).decode('utf8')]}
response = requests.post("http://127.0.0.1:8866/predict/ocr_system",
                         headers={"Content-type": "application/json"},
                         data=json.dumps(data))
print(response.json())
```