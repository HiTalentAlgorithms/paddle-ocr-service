FROM nvcr.io/nvidia/pytorch:24.12-py3

RUN pip install "paddlex[ocr]" paddlepaddle-gpu==3.3.1 --extra-index-url https://www.paddlepaddle.org.cn/packages/stable/cu118/ && paddlex --install serving
# RUN paddlex --install hpi-gpu  显存会增大
COPY PaddleOCR.yaml PaddleOCR.yaml
EXPOSE 8080
CMD ["paddlex", "--serve", "--pipeline", "PaddleOCR.yaml"]
