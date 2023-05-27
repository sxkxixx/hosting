FROM python:3.10-alpine

WORKDIR app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade setuptools
RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt