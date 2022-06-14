FROM python:alpine3.16
WORKDIR /app
COPY  requirements.txt ./
RUN pip install -r requirements.txt
RUN mkdir templates && mkdir static
COPY main.py mongo.py ./
RUN chmod +x main.py
COPY templates/* ./templates/
COPY static/* ./static/
EXPOSE 8080
CMD ["python3", "main.py"]