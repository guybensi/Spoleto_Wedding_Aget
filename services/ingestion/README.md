# Ingestion Service

This directory will contain the Python support service responsible for:

- file intake and manifests
- OCR and vision-orchestrated extraction
- normalization into canonical trip schemas
- provenance capture
- publish workflows for retrieval-ready knowledge bundles

The first executable implementation slice for this service will add:

1. a Python package skeleton
2. schema definitions
3. fixture-based tests for source normalization

## Current implementation

The repository now includes a manifest loader for raw source documents. It validates:

- trip id presence
- non-empty document lists
- allowed document types
- allowed source file formats

The next step is to extend this into typed normalization and ingestion pipelines.

