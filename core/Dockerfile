FROM python:3.9-alpine
LABEL maintainer="Max <evtushenkodev@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN apk add python3-dev build-base linux-headers pcre-dev
RUN pip install uwsgi

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
