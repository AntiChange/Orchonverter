# Dockerfile, Image, Container
FROM python:2.7

WORKDIR /flask-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src .

# RUN apk add --no-cache python2

CMD [ "python", "./app.py"]