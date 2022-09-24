FROM python:alpine3.16
WORKDIR /app
COPY  requirements.txt ./
RUN pip install -r requirements.txt
CMD ["python3", "E2E.py", $1]