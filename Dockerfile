FROM python:3.8-slim
ADD etc_files/sources.list /etc/apt/sources.list
RUN pip install -U pip
ADD requirements.txt /opt/image2pdf/requirements.txt
COPY etc_files/tesseract.tar.gz /opt/tesseract/tesseract.tar.gz
WORKDIR /opt/tesseract
RUN apt update \
    && apt install gcc g++ make libmagic-dev automake libtool pkg-config libleptonica-dev -y \
    && tar zxvf tesseract.tar.gz \
    && cd tesseract-5.0.0-alpha-20201224 \
    && ./autogen.sh \
    && ./configure \
    && make && make install \
    && ldconfig \
    && cd /opt/image2pdf \
    && pip install cmake==3.18.4.post1 -i https://mirrors.aliyun.com/pypi/simple \
    && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
    && apt install libgomp1 -y \
    && apt --purge remove gcc g++ make automake libtool pkg-config -y \
    && apt autoremove -y \
    && apt clean \
    && rm -rf /opt/tesseract/ \
    && rm -rf /root/.cache
ADD src /opt/image2pdf
WORKDIR /opt/image2pdf
ADD model2/chi_sim.traineddata /usr/local/share/tessdata/chi_sim.traineddata
ADD etc_files/pdf.ttf /usr/local/share/tessdata/pdf.ttf
ENV TEMPDIR=/tmp/ TESSERACT_CMD=tesseract TESSDATA_PREFIX=/usr/local/share/tessdata

EXPOSE 5000
CMD ["python","app.py"]