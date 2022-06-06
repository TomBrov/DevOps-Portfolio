FROM python:alpine3.16
WORKDIR /app
COPY main.py mongo.py requirements.txt ./
RUN pip install -r requirements.txt && chmod +x main.py
RUN mkdir templates && mkdir static
COPY templates/* ./templates/
COPY static/* ./static/
EXPOSE 8080
CMD ["python3", "main.py"]