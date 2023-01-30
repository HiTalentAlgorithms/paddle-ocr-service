## Clone 
```
git clone https://github.com/HiTalentAlgorithms/paddle-ocr-service.git
```

## Configuration
Workdir of the ocr service is `/PaddleOCR/deploy/pdserving`,Mounting Configuration files must be mounted to this directory

HTTP Server port is 8866, Grpc Server port is 18091


## [CPU]Build and run
```
docker build -t minghealtomni/paddle-ocr .
docker run -d -p 8866:8866 -p 18091:18091 --name 'ocr-service' minghealtomni/paddle-ocr
```
## [GPU]Build and run
```
docker build -t minghealtomni/paddle-ocr-gpu -f Dockerfile_GPU .
docker run --name paddle-ocr-gpu -dp 8866:8866 -p 18091:18091 --rm --gpus all --pid=host  minghealtomni/paddle-ocr-gpu 
```

## python grpc request

```python
import json
import grpc
from grpc_client.pipeline_client import PipelineClient
from grpc._channel import _InactiveRpcError
import base64


client = PipelineClient()
client.connect(['127.0.0.1:18091'])
with open("image0.png", "rb") as f:
    content = f.read()
try:
    ret = client.predict(feed_dict={"image": base64.b64encode(content).decode('utf8')}, timeout=30)
    print(json.loads(ret.value[0]))
except _InactiveRpcError as e:
    # if set timeout, and operating time timeout
    if e.code() is grpc.StatusCode.DEADLINE_EXCEEDED:
        print('ocr grpc server timeout')
    else:
        print('other error')
    raise e

```

## python http request
### API Url: /ocr/prediction
    Methods:
        Post: Extract text from PDF images using Paddle OCR
            Request: {"key": ["image"], "value": ["base64 of image"]}
            Response: image text json

```python
import base64
import json
import requests


with open("image0.png", "rb") as f:
    content = f.read()
data = {"key": ["image"], "value": [base64.b64encode(content).decode('utf8')]}
response = requests.post("http://127.0.0.1:8886/ocr/prediction",
                         headers={"Content-type": "application/json"},
                         data=json.dumps(data))
print(json.loads(response.json()['value'][0]))
```