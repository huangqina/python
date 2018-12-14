FROM ubuntu:16.04


COPY requirements.txt ./
COPY interface.py ./
COPY con2.py ./
COPY gunicorn.conf.py ./
COPY config ./
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


