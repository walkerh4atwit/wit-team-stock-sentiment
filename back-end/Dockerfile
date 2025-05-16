FROM python:3.11.11-slim

WORKDIR /back-end

ADD back-end/src src
ADD backend_util backend_util
ADD back-end/queries queries
ADD back-end/requirements-unix.txt .

RUN ["sh", "-c", "pip install --upgrade -v pip"]
RUN ["sh", "-c", "pip install -r requirements-unix.txt"]
# RUN ["sh", "-c", "export "]

ENTRYPOINT ["sh", "-c", "export PYTHONPATH=src && gunicorn --capture-output -b :8000 --workers=3 src.wsgi:app"]