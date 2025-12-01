FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system dependencies (optional: for fonts, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY web/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create user and group
RUN groupadd -g 1003 psacln && useradd -u 10000 -g 1003 -m webadmin

# Copy the rest of the app
COPY web/app ./app
COPY web/assets ./assets
COPY web/dashboards ./dashboards

# Set permissions for the app files
RUN chown -R webadmin:psacln /app

# Expose Panel port
EXPOSE 5013

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV BINANCE_API_KEY=${BINANCE_API_KEY:-}

# Start the Panel app using launch.py
CMD ["python", "app/launch.py"]