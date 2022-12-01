FROM python:3.9-slim-buster

WORKDIR /opt

COPY ./requirements.txt requirements.txt
COPY ./app .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV BACKGROUND_COLOR="blue"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80