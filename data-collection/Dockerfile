FROM python:3.11.11-slim

ADD src/* .
ADD requirements-unix.txt .

RUN ["/bin/sh", "pip3", "install", "--upgrade", "-v", "pip"]

ENTRYPOINT ["/bin/sh", "pip3", "install", "-r", "requirements-unix.txt", "&&", \
    "python3", "alpaca_collector.py"]