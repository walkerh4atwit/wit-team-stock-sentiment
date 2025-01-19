FROM python:3.11.11-slim

ADD src/* .
ADD requirements-unix.txt .

RUN ["sh", "-c", "pip install --upgrade -v pip"]
RUN ["sh", "-c", "pip install -r requirements-unix.txt"]

ENTRYPOINT ["sh", "-c", "python alpaca_collector.py"]