FROM python:alpine3.16
WORKDIR /app
COPY  requirements.txt entrypoint.sh E2E.py ./
RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/sh", "entrypoint.sh"]