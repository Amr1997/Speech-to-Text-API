FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY speach_text/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script
COPY speach_text/docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Copy project files
COPY speach_text/ /app/

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]