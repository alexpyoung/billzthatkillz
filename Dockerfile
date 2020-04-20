FROM python:3.8

RUN apt-get update && apt-get install -y \
    poppler-utils \
    python3-pil \
    tesseract-ocr
RUN mkdir -p /opt/btk/
WORKDIR /opt/btk
COPY requirements.txt ./
RUN pip install --upgrade -r requirements.txt

COPY . ./

CMD ["python", "-m", "main"]
