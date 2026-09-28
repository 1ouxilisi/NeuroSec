FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt fastapi uvicorn

COPY pentestai/ ./pentestai/
COPY web/ ./web/
COPY neurosec.py .

EXPOSE 8000

CMD ["python", "web/app.py"]
