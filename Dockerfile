FROM python:3.11-slim

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements ./requirements

RUN pip install -r ./requirements/base.txt

COPY . .

CMD ["gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:80"]
