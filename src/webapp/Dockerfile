
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

#Install Python dependencies to /opt/venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.11-slim

# make a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy Python virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

COPY --chown=appuser:appuser . .

ENV PATH="/opt/venv/bin:$PATH"


ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


EXPOSE 5000

USER appuser

#HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    #CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Run application
CMD ["python", "app.py"]