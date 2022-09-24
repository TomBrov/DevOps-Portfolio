FROM python:alpine3.16
WORKDIR /app
COPY  requirements.txt entrypoint.sh ./
RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/sh", "entrypoint.sh"]