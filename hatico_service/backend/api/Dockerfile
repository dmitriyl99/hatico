FROM python:3.7-slim


RUN apt-get update && apt-get install -y python3-pymongo


COPY ./app /app
COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV HOST 0.0.0.0
ENV PORT 80

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
