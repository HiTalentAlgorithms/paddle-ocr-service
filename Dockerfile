FROM paddlepaddle/paddle:2.2.2

RUN pip3.7 install --upgrade pip &&\
    python3.7 -m pip install paddlepaddle &&\
    pip3.7 install paddlehub --upgrade


RUN git clone https://github.com/PaddlePaddle/PaddleOCR.git
RUN cd PaddleOCR
RUN git checkout -b release/2.4 origin/release/2.4
RUN pip3.7 install -r requirements.txt

RUN mkdir -p /PaddleOCR/inference/
ADD ch_ppocr_mobile_v2.0_cls_infer.tar /PaddleOCR/inference/
ADD ch_PP-OCRv2_rec_infer.tar /PaddleOCR/inference/
ADD ch_PP-OCRv2_det_infer.tar /PaddleOCR/inference/
ENV FLASK_ENV=server
RUN hub install deploy/hubserving/ocr_system/
EXPOSE 8866

CMD ["/bin/bash","-c","hub serving start -m ocr_system"]