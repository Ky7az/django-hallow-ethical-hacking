FROM python:3.9.9-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./entrypoint.sh ./
COPY . ./

ENTRYPOINT ["/app/entrypoint.sh"]