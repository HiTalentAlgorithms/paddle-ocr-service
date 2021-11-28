FROM paddlepaddle/paddle:2.1.1

RUN pip3.7 install --upgrade pip &&\
    python3.7 -m pip install paddlepaddle==2.1.1 &&\
    pip3.7 install paddlehub --upgrade

ADD paddle.tar /
RUN mv /PaddleOCR-2.1.1 /PaddleOCR
WORKDIR /PaddleOCR
RUN pip3.7 install -r requirements.txt

RUN mkdir -p /PaddleOCR/inference/
ADD ch_ppocr_mobile_v2.0_cls_infer.tar /PaddleOCR/inference/
ADD ch_ppocr_mobile_v2.0_det_infer.tar /PaddleOCR/inference/
ADD ch_ppocr_mobile_v2.0_rec_infer.tar /PaddleOCR/inference/
RUN hub install deploy/hubserving/ocr_system/
EXPOSE 8866

CMD ["/bin/bash","-c","hub serving start -m ocr_system"]