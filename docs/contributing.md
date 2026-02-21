# Contributing

Thanks for contributing to `lakhua`.

## Development setup

Clone the repository and work in the SDK you want to change.

### JavaScript / TypeScript

```bash
cd libs/javascript
bun install
bun run check
```

### Python

```bash
cd libs/python
pip install -e ".[dev]"
pytest
ruff check .
mypy lakhua
```

### Go

```bash
cd libs/go
go test ./...
go vet ./...
```

## Contribution rules

- Keep cross-SDK behavior aligned (defaults, fallback, return shape).
- Prefer backward-compatible changes.
- Add or update tests for behavior changes.
- Keep data files and API docs consistent.
- Avoid adding heavy dependencies without strong reason.

## Pull request checklist

- Tests pass in affected SDK(s).
- Lint/type checks pass where applicable.
- Public docs are updated (`README` or `docs/`).
- Changes are scoped and easy to review.

## Reporting issues

Include:

- Exact input (`lat/lon` or H3 index)
- Expected output and actual output
- SDK + version
- Minimal reproduction snippet

