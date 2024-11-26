FROM python:3.12-slim

RUN apt-get update && apt-get install -y libmagic-dev

WORKDIR /app

COPY /requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .
