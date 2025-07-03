FROM python:3.9-slim

WORKDIR /app

COPY . .

EXPOSE 666

RUN apt update && apt install -y sqlite3 && pip install requests

CMD ["python", "hello-world.py"]