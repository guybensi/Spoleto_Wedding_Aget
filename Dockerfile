FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY README.md /app/README.md
COPY services /app/services
COPY tests /app/tests
COPY data /app/data
COPY prompts /app/prompts
COPY workspace /app/workspace
COPY openclaw /app/openclaw

CMD ["python", "-m", "unittest", "discover", "-s", "tests"]
