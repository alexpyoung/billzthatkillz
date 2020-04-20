FROM python:3.8

RUN apt-get update && apt-get install -y \
    poppler-utils \
    python3-pil \
    tesseract-ocr
RUN pip install money pdf2image pyocr
RUN pip install isort pylint ipython

RUN mkdir -p /opt/btk/
COPY . /opt/btk
RUN ln -s /opt/btk/src/main /usr/local/bin/btk

CMD ["btk"]
