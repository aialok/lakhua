# Getting Started

This guide helps you run `lakhua` quickly in JavaScript, Python, and Go.

## Choose an SDK

- JavaScript / TypeScript: `@aialok/lakhua`
- Python: `lakhua`
- Go: `github.com/aialok/lakhua/libs/go`

## Install

### JavaScript / TypeScript

```bash
npm install @aialok/lakhua
```

### Python

```bash
pip install lakhua
```

### Go

```bash
go get github.com/aialok/lakhua/libs/go
```

## First lookup

### JavaScript / TypeScript

```ts
import { geocode } from "@aialok/lakhua";

const result = geocode(28.6139, 77.2090);
console.log(result);
```

### Python

```python
from lakhua import geocode

result = geocode(28.6139, 77.2090)
print(result)
```

### Go

```go
result := lakhua.Geocode(28.6139, 77.2090, nil)
fmt.Println(result)
```

## Common behavior across SDKs

- First call loads JSON data into memory.
- Subsequent lookups are in-memory map/dict reads.
- Fallback is enabled by default (`5 -> 4` resolution).
- Invalid inputs or missing coverage return `null`/`None`/`nil`.

## Run locally from this repo

### JavaScript

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
```

### Go

```bash
cd libs/go
go test ./...
```

## Next docs

- Architecture: `docs/architecture.md`
- Contribution flow: `docs/contributing.md`
- FAQ: `docs/faq.md`

