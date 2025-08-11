FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirments.txt
COPY app.py .
RUN mkdir -p /var/log/sample_app &&chown -R 1000:1000 /var/log/sample_app
EXPOSE 8000
CMD ["python", "app.py"]
