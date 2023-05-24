FROM python:3.10-alpine

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /code/
COPY . /code/

ENTRYPOINT ["/code/entrypoint.sh"]