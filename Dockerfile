FROM python:3.8-buster

COPY . /SmartHome-Backend
WORKDIR /SmartHome-Backend

RUN pip install psycopg2-binary
RUN pip install -r requirements.txt
RUN pip install gunicorn

# COPY entrypoint.sh /usr/local/bin/

EXPOSE 8000
CMD ["gunicorn"  , "--bind", "0.0.0.0:8000", "flaskr:create_app()"]