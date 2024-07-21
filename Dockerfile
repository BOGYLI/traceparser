FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY __main__.py __main__.py
COPY config.yaml config.yaml

CMD ["python", "__main__.py"]
