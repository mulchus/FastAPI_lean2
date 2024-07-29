FROM python:3.11-slim

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements ./requirements

RUN pip install -r ./requirements/base.txt

COPY . .

RUN chmod a+x ./docker/*.sh
