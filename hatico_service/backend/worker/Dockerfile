FROM python:3.7-slim

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./app /app
COPY ./requirements.txt .

RUN pip install pandas imageai==2.1.6 keras pydantic tensorflow==2.4.0 loguru pymongo opencv-python scikit-learn

CMD python -m app.main
