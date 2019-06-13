FROM python:3.7-alpine

RUN mkdir /var/app

COPY requirements.txt /var/app/requirements.txt

RUN python -m pip install -r /var/app/requirements.txt

COPY fileshelter /var/app/fileshelter

WORKDIR /var/app
CMD python fileshelter/app.py