FROM python:3.9-slim

WORKDIR /opt/minsys-chatai

COPY requirements.txt .
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]