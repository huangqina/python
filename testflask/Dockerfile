FROM ubuntu:16.04

RUN mkdir ./flask
RUN cd flask
COPY requirements.txt ./
COPY app.py ./
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY gunicorn.conf.py ./
