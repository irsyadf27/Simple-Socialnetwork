FROM python:3.7.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update
ADD social_network/requirements.txt social_network/requirements.txt
RUN pip install --no-cache-dir -r social_network/requirements.txt

COPY ./compose/local/django/entrypoint /entrypoint
COPY ./compose/local/django/start /start
RUN chmod +x /entrypoint /start

ADD .env/.local/.django /envs/

# Mount your repo root dire as a volume under /code
RUN mkdir /code
WORKDIR /code

ENTRYPOINT ["/entrypoint"]