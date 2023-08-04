# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python3", "manage.py", "runserver"]