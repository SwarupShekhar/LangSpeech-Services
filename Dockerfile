FROM runpod/pytorch:2.2.1-py3.10-cuda12.1.1-devel-ubuntu22.04

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Expose port 10000 for Render
EXPOSE 10000

CMD ["uvicorn", "app_backend:app", "--host", "0.0.0.0", "--port", "10000"]
