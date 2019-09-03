FROM python:3.6-alpine
MAINTAINER Sajeesh E Namboothiri

ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
#RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser --disabled-password --gecos '' user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user