FROM python:3.11.11-slim

ADD src/* .
ADD requirements-unix.txt .

RUN ["sh", "-c", "pip3 install --upgrade -v pip"]

ENTRYPOINT ["sh", "-c", "pip3 install -r requirements-unix.txt && python3 alpaca_collector.py"]