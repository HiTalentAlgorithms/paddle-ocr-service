# FROM ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlex/paddlex:paddlex3.3.4-paddlepaddle3.2.0-gpu-cuda12.6-cudnn9.5-trt10.5
FROM ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlex/paddlex:paddlex3.0.1-paddlepaddle3.0.0-gpu-cuda11.8-cudnn8.9-trt8.6
RUN paddlex --install serving && paddlex --install hpi-gpu
COPY PaddleOCR.yaml PaddleOCR.yaml
EXPOSE 18092
CMD ["paddlex", "--serve", "--pipeline", "PaddleOCR.yaml"]

