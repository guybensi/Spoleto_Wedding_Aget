# Deployment Baseline

This repository now includes the first packaging baseline for local development and VPS deployment.

## Files

- `.env.example` documents expected runtime variables.
- `Dockerfile` packages the Python ingestion slice and can run the current test suite.
- `docker-compose.yml` defines two service boundaries:
  - `openclaw` for the conversational runtime
  - `ingestion` for Python ingestion tasks

## Current intent

These assets are intentionally minimal. They establish the deployment shape before the final runtime entrypoints are implemented.

## Secrets policy

- Do not commit `.env`.
- Use `.env.example` as a documentation template only.
- Production secrets should come from the host environment, a secret manager, or deployment-platform secret storage.

## Next packaging steps

1. Add an actual Python package install path to the Dockerfile.
2. Add health checks and explicit OpenClaw runtime commands.
3. Add a VPS deployment runbook and backup instructions.
4. Add compose profiles for staging and production differences.
