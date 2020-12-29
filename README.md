# image2pdf

#### API Url: /image2pdf 
    Methods:
        Post: Extract text from PDF or PDF images using OCR
            Request: {"file": "file content"}
            Response: pdf file content
        
#### API Url: /pdf2image 
    Methods:
        Post: Convert PDF to a single long image
            Request: {"file": "file content"}
            Response: image file content
        
#### API Url: /faceImages 
    Methods:
        Post: Extract PDF images with faces
            Request: {"file": "file content"}
            Response: {"images":"Base64 list of images"}