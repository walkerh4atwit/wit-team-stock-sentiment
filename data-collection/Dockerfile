FROM python:3.11.11-slim

WORKDIR /data-collection

ADD backend_util backend_util
ADD data-collection/src src
ADD data-collection/requirements-unix.txt .

RUN ["sh", "-c", "pip install --upgrade -v pip"]
RUN ["sh", "-c", "pip install -r requirements-unix.txt"]
RUN ["sh", "-c", "export PYTHONPATH='..'"]

ENTRYPOINT ["sh", "-c", "python src/alpaca_collector.py"]