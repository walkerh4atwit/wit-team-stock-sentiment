FROM python:alpine

ADD src/* .
ADD requirements-unix.txt .

RUN pip install --upgrade pip

ENTRYPOINT ["sh", "pip install -r requirements-unix.txt && \
    python alpaca_collector.py"]