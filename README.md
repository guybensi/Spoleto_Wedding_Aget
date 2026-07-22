# Spoleto Wedding Agent

Production-oriented project scaffold for a private WhatsApp travel assistant for a wedding trip in Spoleto, Umbria.

## Current scope

- OpenClaw-based runtime with the native WhatsApp plugin
- Claude model integration via Anthropic API
- Python-based ingestion support for PNG, PDF, and spreadsheet trip materials
- Docker-first deployment target for a single Linux VPS
- Externalized prompt architecture and modular OpenClaw configuration

## Repository layout

- `docs/specification/` - architecture and delivery documentation
- `openclaw/` - gateway configuration skeleton
- `workspace/` - bootstrap files injected into agent context
- `prompts/base/` - modular prompt files assembled at runtime
- `services/ingestion/` - ingestion service placeholder and contracts
- `data/` - permanent and trip-specific knowledge roots
- `tests/` - executable repository contract tests

## Validation

Run the scaffold contract test:

```powershell
py -3 -m unittest tests.test_scaffold
```

## Next implementation slices

1. Add CI to enforce the scaffold contract.
2. Implement structured trip schemas and ingestion manifests.
3. Add OpenClaw environment examples and deployment assets.
4. Build the Python ingestion package with unit-tested normalization code.
