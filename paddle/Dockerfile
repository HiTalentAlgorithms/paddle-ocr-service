FROM hub.baidubce.com/paddlepaddle/paddle:latest-gpu-cuda10.0-cudnn7-dev

RUN pip3.7 install --upgrade pip -i https://mirror.baidu.com/pypi/simple

RUN python3.7 -m pip install paddlepaddle==2.0.0rc0 -i https://mirror.baidu.com/pypi/simple

RUN pip3.7 install paddlehub --upgrade -i https://mirror.baidu.com/pypi/simple

#RUN git clone https://github.com/PaddlePaddle/PaddleOCR.git /PaddleOCR
ADD PaddleOCR-release-2.0-rc1-0.zip /
RUN mv PaddleOCR-release-2.0-rc1-0 PaddleOCR
WORKDIR /PaddleOCR

RUN pip3.7 install -r requirements.txt -i https://mirror.baidu.com/pypi/simple

RUN mkdir -p /PaddleOCR/inference/
ADD ch_ppocr_mobile_v2.0_cls_infer.tar /PaddleOCR/inference/
ADD ch_ppocr_mobile_v2.0_det_infer.tar /PaddleOCR/inference/
ADD ch_ppocr_mobile_v2.0_rec_infer.tar /PaddleOCR/inference/

EXPOSE 8868

CMD ["/bin/bash","-c","hub install deploy/hubserving/ocr_system/ && hub serving start -m ocr_system"]