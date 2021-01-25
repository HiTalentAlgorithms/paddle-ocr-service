FROM paddlepaddle/paddle:latest-dev-cuda10.1-cudnn7-gcc82

RUN pip3.7 install --upgrade pip &&\
    python3.7 -m pip install paddlepaddle==2.0.0rc1 &&\
    pip3.7 install paddlehub --upgrade

ADD paddle.tar /
RUN mv /PaddleOCR-release-2.0-rc1-0 /PaddleOCR
WORKDIR /PaddleOCR
RUN pip3.7 install -r requirements.txt

RUN mkdir -p /PaddleOCR/inference/
ADD ch_ppocr_mobile_v2.0_cls_infer.tar /PaddleOCR/inference/
ADD ch_ppocr_mobile_v2.0_det_infer.tar /PaddleOCR/inference/
ADD ch_ppocr_mobile_v2.0_rec_infer.tar /PaddleOCR/inference/

EXPOSE 8866

CMD ["/bin/bash","-c","hub install deploy/hubserving/ocr_system/ && hub serving start -m ocr_system"]