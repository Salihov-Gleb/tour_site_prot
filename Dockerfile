FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYCODE=1
WORKDIR /app

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev


RUN apk --update add \
    build-base \
    jpeg-dev \
    zlib-dev


RUN pip install --upgrade pip
COPY requirements.txt .
COPY entrypoint.sh .

RUN apk add postgresql-dev gcc
RUN pip install -r ./requirements.txt
RUN chmod +x entrypoint.sh

COPY . .

EXPOSE 8000

ENTRYPOINT [ "/app/entrypoint.sh" ]