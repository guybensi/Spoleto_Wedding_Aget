# Testing Strategy

This repository uses executable tests to lock in each implementation slice before broader feature work lands.

## Current test layers

- Scaffold contract tests verify the required repository layout.
- Ingestion manifest tests verify source-document metadata validation.
- Automation contract tests verify CI and contributor guidance stay present.

## Local command

```powershell
py -3 -m unittest discover -s tests
```

## Expansion plan

Next test layers should cover:

1. schema validation for normalized trip records
2. prompt assembly behavior
3. OpenClaw config sanity checks
4. ingestion pipeline fixtures for OCR and normalization
5. deployment smoke tests for containerized runtime assets
