FROM python:3.8-buster

COPY . /app
WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]