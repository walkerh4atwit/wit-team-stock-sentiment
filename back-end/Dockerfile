FROM python:3.11.11-slim
WORKDIR /back-end
ADD src/* .
ADD queries queries
ADD requirements-unix.txt .

# RUN which python | ls -la
# RUN ["/bin/sh", "ls", "-la"]
RUN ["sh", "-c", "pip install --upgrade -v pip"]

ENTRYPOINT ["sh", "-c", "pip install -r requirements-unix.txt && gunicorn --capture-output -b :8000 --workers=3 wsgi:app"]