FROM python:3.10-slim

WORKDIR /app

# Ensure logs are visible in Cloud Run
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y git gcc && rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn

COPY . .

# Cloud Run uses PORT environment variable
ENV PORT=8080
EXPOSE 8080

# Run the application using the generated main.py which handles env vars
CMD ["python", "main.py"]
