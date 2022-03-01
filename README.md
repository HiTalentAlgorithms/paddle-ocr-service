# image2pdf

## docker build
require git lfs (https://github.com/git-lfs/git-lfs)
```
git clone https://github.com/HiTalentAlgorithms/paddle-ocr-service.git
git lfs pull
```
or 
```
git lfs clone https://github.com/HiTalentAlgorithms/paddle-ocr-service.git
```

#### API Url: /predict/ocr_system 
    Methods:
        Post: Extract text from PDF images using Paddle OCR
            Request: {"images": ["base64 of image"]}
            Response: image text json
  
#### run
```shell
docker run -d -p 8866:8866 --name 'ocr-service' minghealtomni/paddle-ocr
```
