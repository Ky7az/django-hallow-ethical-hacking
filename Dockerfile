FROM python:3.14.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME=/app
ENV APP_USER=appuser

RUN addgroup -S "$APP_USER" && adduser -H -D -S -G "$APP_USER" "$APP_USER"

WORKDIR $APP_HOME

# hadolint ignore=DL3013,DL3018
RUN apk update && apk --no-cache add gcc musl-dev postgresql-dev python3-dev && pip install --no-cache-dir --upgrade pip
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh ./
COPY . ./

RUN python3 manage.py collectstatic --no-input --clear && chown -R "$APP_USER":"$APP_USER" "$APP_HOME"
USER $APP_USER

HEALTHCHECK CMD python3 manage.py health_check || exit 1
ENTRYPOINT ["/app/entrypoint.sh"]
