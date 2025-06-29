FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# Set environment variables placeholders (these will be set by Render)
ENV EMAIL_USER=""
ENV EMAIL_PASS=""

# Copy app code
COPY . .

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose is optional on Render
EXPOSE 7860

# Run server
CMD ["uvicorn", "backend_ports:app", "--host", "0.0.0.0", "--port", "7860"]