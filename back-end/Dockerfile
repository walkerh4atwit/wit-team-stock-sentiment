FROM python:3.11.11-slim
WORKDIR /back-end
ADD src/* .
ADD queries queries
ADD requirements-unix.txt .

RUN uname -m
RUN pip3 install --upgrade -v pip

ENTRYPOINT pip3 install -r requirements-unix.txt && \
    gunicorn -b :8000 --workers=3 wsgi:app