FROM paddlepaddle/paddle:2.3.1
# gpu
# FROM paddlepaddle/paddle:2.3.1-gpu-cuda11.2-cudnn8

RUN git clone -b release/2.5 https://github.com/PaddlePaddle/PaddleOCR.git /PaddleOCR
WORKDIR /PaddleOCR
RUN pip3.7 install -r requirements.txt

# cpu
RUN pip3.7 install paddle-serving-server paddle-serving-client paddle-serving-app
# gpu
# RUN pip3.7 install paddle-serving-server-gpu paddle-serving-client paddle-serving-app

WORKDIR /PaddleOCR/deploy/pdserving/
RUN wget https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar -O ch_PP-OCRv3_det_infer.tar && tar -xf ch_PP-OCRv3_det_infer.tar
RUN wget https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar -O ch_PP-OCRv3_rec_infer.tar &&  tar -xf ch_PP-OCRv3_rec_infer.tar
RUN python3 -m paddle_serving_client.convert --dirname ./ch_PP-OCRv3_det_infer/ \
                                             --model_filename inference.pdmodel          \
                                             --params_filename inference.pdiparams       \
                                             --serving_server ./ppocr_det_v3_serving/ \
                                             --serving_client ./ppocr_det_v3_client/
RUN python3 -m paddle_serving_client.convert --dirname ./ch_PP-OCRv3_rec_infer/ \
                                             --model_filename inference.pdmodel          \
                                             --params_filename inference.pdiparams       \
                                             --serving_server ./ppocr_rec_v3_serving/  \
                                             --serving_client ./ppocr_rec_v3_client/
ADD pdserving/config.yml /PaddleOCR/deploy/pdserving/config.yml
ADD pdserving/web_service.py /PaddleOCR/deploy/pdserving/web_service.py
EXPOSE 8866

CMD ["python3", "web_service.py"]