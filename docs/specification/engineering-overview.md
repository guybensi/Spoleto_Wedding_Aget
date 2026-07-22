# Engineering Overview

This repository implements the foundation for the Spoleto wedding travel assistant.

## Architecture baseline

- OpenClaw is the primary conversational runtime.
- The native WhatsApp plugin is the messaging transport.
- Anthropic Claude models handle reasoning and response generation.
- Python support services handle ingestion, OCR orchestration, normalization, and publish workflows.
- Private trip documents are the authoritative source over public web results.

## Initial repository goals

- Establish the permanent repository layout.
- Externalize prompts and agent bootstrap instructions.
- Add OpenClaw config placeholders that can be expanded without restructuring the repo.
- Introduce executable tests that guard the project scaffold.
- Document the boundaries between runtime, data, prompts, and ingestion.

## Delivery strategy

The first milestone focuses on structure, documentation, and testability rather than feature-complete runtime behavior. That keeps the project auditable while later slices add ingestion code, CI, and deployment assets.
