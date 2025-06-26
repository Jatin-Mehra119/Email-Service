FROM python:3.12-slim

WORKDIR /app

# Create non-root user first
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# Accept the secret token as a build argument
ARG EMAIL_USER
ARG EMAIL_PASS

# Expose the secret EMAIL_USER at build time and set them as environment variables
RUN --mount=type=secret,id=EMAIL_USER,mode=0444,required=true \
    export EMAIL_USER=$(cat /run/secrets/EMAIL_USER) && \
    echo "EMAIL_USER is set."

# Expose the secret EMAIL_PASS at build time and set them as environment variables
RUN --mount=type=secret,id=EMAIL_PASS,mode=0444,required=true \
    export EMAIL_PASS=$(cat /run/secrets/EMAIL_PASS) && \
    echo "EMAIL_PASS is set."

# Set environment variables
ENV PYTHONPATH=/app \
    PATH=/usr/local/bin:$PATH

# Copy application code
COPY . .

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose Port 7860 for the FastAPI server
EXPOSE 7860

# Run the fastapi server using uvicorn
CMD ["uvicorn", "backend_ports:app", "--host", "0.0.0.0", "--port", "7860"]