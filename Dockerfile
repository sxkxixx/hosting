FROM python:3.10

WORKDIR /application

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY . .

CMD ["gunicorn","app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]