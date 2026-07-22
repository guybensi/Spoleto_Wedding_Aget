# Contributing

## Working rules for this repository

1. Add or update tests before landing significant runtime or config changes.
2. Run the test suite locally before every commit.
3. Keep prompts, config, ingestion logic, and documentation in sync.
4. Prefer small, reviewable commits that match one implementation slice.
5. Avoid committing secrets, raw guest-private data, or provider credentials.

## Local validation

Run the current test suite from the repository root:

```powershell
py -3 -m unittest discover -s tests
```

## Commit guidance

- Commit repository structure changes separately from runtime logic when practical.
- Write commit messages that describe the delivered slice, for example `Add ingestion manifest contract`.
- Push validated changes promptly so the remote stays usable as the project source of truth.

## Documentation expectations

Update the relevant files when changing architecture or behavior:

- `README.md`
- `docs/specification/`
- `project-onboarding-checklist.txt`
- prompt and workspace instruction files
