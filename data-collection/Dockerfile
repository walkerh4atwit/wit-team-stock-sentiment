FROM python:3.11.11-slim

ADD src/* .
ADD requirements-unix.txt .

RUN pip3 install --upgrade pip

ENTRYPOINT pip3 install -r requirements-unix.txt && \
    python3 alpaca_collector.py