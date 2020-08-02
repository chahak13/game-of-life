# syntax=docker/dockerfile:1.0.0-experimental
FROM python:3.7.0-slim

RUN apt-get update && apt-get install -y tree
COPY requirements.txt /life/requirements.txt
RUN python -m pip install --requirement /life/requirements.txt
COPY . /life

WORKDIR /life
CMD ["echo", "Docker image build. Please run with input file"]
