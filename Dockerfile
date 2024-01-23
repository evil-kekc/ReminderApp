FROM python:3.10-slim-buster
LABEL authors="artem.troshkin"

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update -y && \
    apt-get install -y curl

COPY app/ .

CMD ["python", "main.py"]
