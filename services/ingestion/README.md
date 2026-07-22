# Ingestion Service

This package implements the first runnable ingestion MVP.

## Capabilities

- CLI intake of PNG files from `data/raw/images`
- Provider interface for OCR/vision extraction
- Mock provider for local testing with no API calls
- Normalization and validation into canonical schemas
- JSON output written to `data/processed`

## Commands

Install editable package from repository root:

```powershell
py -3.11 -m pip install -e .
```

Run ingestion with the mock provider:

```powershell
spoleto-ingest --input-dir data/raw/images --output-dir data/processed --provider mock
```

Assemble modular prompts:

```powershell
spoleto-assemble-prompt --base-dir prompts/base --output workspace/system_prompt.md
```

Validate startup prerequisites:

```powershell
spoleto-validate-startup --root .
```

