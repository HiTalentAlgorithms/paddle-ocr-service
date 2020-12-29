FROM python:3.8-slim
ADD sources.list /etc/apt/sources.list
ADD tesseract.tar.gz /opt/tesseract/tesseract.tar.gz
RUN apt update
RUN apt install gcc g++ make libmagic-dev automake libtool pkg-config libleptonica-dev -y
WORKDIR /opt/tesseract/tesseract.tar.gz/tesseract-5.0.0-alpha-20201224
RUN ./autogen.sh
RUN ./configure
RUN make && make install
RUN ldconfig
RUN pip install -U pip
ADD requirements.txt /opt/image2pdf/requirements.txt
WORKDIR /opt/image2pdf
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
ADD src /opt/image2pdf
ADD model2/chi_sim.traineddata /usr/local/share/tessdata/chi_sim.traineddata
ENV TEMPDIR=/tmp/ TESSERACT_CMD=tesseract TESSDATA_PREFIX=/usr/local/share/tessdata

EXPOSE 5000
CMD ["gunicorn","-c","gunicorn.py","app:app"]