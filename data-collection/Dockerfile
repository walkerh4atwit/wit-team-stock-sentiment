FROM python:3.11.11-slim

ADD src/* .
ADD requirements-unix.txt .

RUN pip install --upgrade pip

ENTRYPOINT pip install -r requirements-unix.txt && \
    python alpaca_collector.py