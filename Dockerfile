FROM python:3.7-alpine

RUN mkdir /var/app

COPY requirements.txt /var/app

RUN python -m pip install -r /var/app/requirements.txt

COPY fileshelter /var/app

CMD python /var/app/app.py