# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . /app
RUN pip install flask && apt-get update && apt-get install -y sqlite3

EXPOSE 5000

CMD ["python", "app.py"]