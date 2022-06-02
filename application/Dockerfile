FROM python:alpine3.16
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt && chmod +x main.py
EXPOSE 8080
CMD ["python", "main.py"]