FROM python:3.9-slim-buster

WORKDIR /user/src/app

RUN pip install --upgrade pip

COPY ./src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000