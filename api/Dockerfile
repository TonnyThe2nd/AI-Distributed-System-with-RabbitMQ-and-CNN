FROM python:3.11-slim

WORKDIR /app

COPY api/requirements.txt .

RUN pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

COPY . .

CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]