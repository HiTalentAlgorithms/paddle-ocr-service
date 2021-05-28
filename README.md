# image2pdf

#### API Url: /predict/ocr_system 
    Methods:
        Post: Extract text from PDF images using Paddle OCR
            Request: {"images": ["base64 of image"]}
            Response: image text json
  
#### run
```shell
docker run -d -p 8866:8866 --name 'ocr-service' minghealtomni/paddle-ocr
```
