FROM python:3.11-slim

# Create app directory and set permissions
RUN mkdir -p /app && \
    # Create a non-root user
    useradd -m appuser && \
    # Set ownership of /app to appuser
    chown -R appuser:appuser /app

WORKDIR /app

# Copy requirements first for better layer caching
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY --chown=appuser:appuser . .

# Create the agents directory and ensure it's writable
RUN mkdir -p /app/agents && \
    chown -R appuser:appuser /app/agents && \
    chmod 755 /app/agents

# Switch to non-root user
USER appuser

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
