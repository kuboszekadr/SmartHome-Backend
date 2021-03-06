FROM python:3.8-slim

COPY . /SmartHome-Backend
WORKDIR /SmartHome-Backend

# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["gunicorn"  , "--bind", "0.0.0.0:8000", "flaskr:create_app()"]