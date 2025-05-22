# Use a minimal base image
FROM python:3.11-slim

# Define build-time variable and set it as an environment variable
ARG VERSION
ENV VERSION=$VERSION

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose the Flask default port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
