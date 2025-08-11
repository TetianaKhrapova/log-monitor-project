FROM python:3.10-slim
WORKDIR /monitor
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY monitor.py .
COPY config.yaml /etc/logmonitor/config.yaml
CMD ["python", "monitor.py"]
