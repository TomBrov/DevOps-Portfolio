FROM python:alpine3.16
WORKDIR /app
COPY  requirements.txt ./
RUN pip install -r requirements.txt && chmod +x main.py
RUN mkdir templates && mkdir static
COPY main.py mongo.py ./
COPY templates/* ./templates/
COPY static/* ./static/
EXPOSE 8080
CMD ["python3", "main.py"]