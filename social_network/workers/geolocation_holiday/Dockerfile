FROM python:3.8.4

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3-pip

COPY workers/geolocation/requirements.txt workers/geolocation/requirements.txt
RUN python3.8 -m pip install -r workers/geolocation/requirements.txt

RUN adduser --disabled-password --gecos "" worker
USER worker

COPY tasks/geolocation.py tasks/geolocation.py
COPY workers/geolocation workers/geolocation

CMD ["celery", "--app", "workers.geolocation", "worker", "-c", "100", "-P", "eventlet", "--loglevel=INFO", "-Q", "geolocation"]
