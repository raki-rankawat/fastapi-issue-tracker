FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY app/ ./app/

# Shell form so ${PORT} (set by hosts like Render) expands; falls back to 8000
# locally. `exec` replaces the shell with uvicorn so it receives stop signals.
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}