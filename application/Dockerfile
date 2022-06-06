FROM python:alpine3.16
WORKDIR /app
COPY main.py mongo.py requirements.txt ./
RUN mkdir templates
COPY templates/* templates/
RUN pip install -r requirements.txt && chmod +x main.py
EXPOSE 8080
CMD ["python3", "main.py"]