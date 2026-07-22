FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY README.md /app/README.md
COPY services /app/services
COPY tests /app/tests
COPY data /app/data
COPY prompts /app/prompts
COPY workspace /app/workspace
COPY openclaw /app/openclaw

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -e .

CMD ["spoleto-ingest", "--input-dir", "/app/data/raw/images", "--output-dir", "/app/data/processed", "--provider", "mock"]
