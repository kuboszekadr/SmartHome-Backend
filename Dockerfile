FROM python:3.8-buster

COPY . /SmartHome-Backend
WORKDIR /SmartHome-Backend

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["gunicorn"  , "--bind", "0.0.0.0:8000", "flaskr:create_app()"]