FROM python:3.9-slim

RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean


RUN apt-get install -y git
RUN git clone https://github.com/vishnubob/wait-for-it.git /wait-for-it


WORKDIR /scrappy

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

WORKDIR /scrappy/flatcrawler

