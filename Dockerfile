FROM python:3.8-alpine
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk add --update bash \
    tesseract-ocr \
    libmagic

ADD requirements.txt /opt/image2pdf/requirements.txt
WORKDIR /opt/image2pdf
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ADD src /opt/image2pdf
ADD model/chi_sim.traineddata /usr/share/tessdata/chi_sim.traineddata
ENV TEMPDIR=/tmp/ TESSERACT_CMD=tesseract

EXPOSE 5000
CMD ["gunicorn","-c","gunicorn.py","app:app"]