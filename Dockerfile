# Dockerfile by @portalsoup - Thank you!
FROM python:3.12-slim

ENV PYTHONPATH=/app/src

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

# RUN poe test

CMD ["python", "rotanika.py"]
