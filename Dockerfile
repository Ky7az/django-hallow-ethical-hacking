FROM python:3.9.9-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./
RUN python manage.py collectstatic --no-input --clear

EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "DjangoHallow.wsgi"]