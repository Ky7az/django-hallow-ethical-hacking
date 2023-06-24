FROM python:3.9.16-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# hadolint ignore=DL3018
RUN apk update && apk --no-cache add postgresql-dev gcc python3-dev musl-dev libffi-dev make rust cargo
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh ./
COPY . ./

ENTRYPOINT ["/app/entrypoint.sh"]