# lakhua

Sub-millisecond reverse geocoding for India. Runs entirely in-memory — zero API calls, zero network, zero latency overhead.

`lakhua` is named after my hometown — a small town barely on most maps.

[![npm](https://img.shields.io/npm/v/@aialok/lakhua)](https://www.npmjs.com/package/@aialok/lakhua)
[![PyPI](https://img.shields.io/pypi/v/lakhua)](https://pypi.org/project/lakhua/)
[![Go](https://img.shields.io/badge/go-pkg.go.dev-blue)](https://pkg.go.dev/github.com/aialok/lakhua/libs/go)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![CI](https://github.com/aialok/lakhua/actions/workflows/ci.yml/badge.svg)](https://github.com/aialok/lakhua/actions/workflows/ci.yml)

---

## What It Does

- 📍 converts `lat, lon` to India location metadata (`city`, `state`, optional `district`, `pincode`)
- 🔢 supports direct H3 index lookup
- ↩️ uses parent-cell fallback (`5 → 4`) when exact cells are missing
- ⚡ loads dataset once in memory — all subsequent lookups are in-memory map operations
- 🐛 optional debug mode to trace load and lookup timings

## What It Does Not Do

- global reverse geocoding (India dataset only)
- address-level precision (city/district level)
- online API or hosted endpoint
- guaranteed full spatial coverage for every coordinate in India

## How It Works

lakhua uses [Uber's H3](https://h3geo.org/) hexagonal grid to index India's geographic data.

1. On first call, it reads two JSON files (`res 4` and `res 5`) into memory.
2. Your coordinates are converted to an H3 cell at resolution 5.
3. It looks up that cell in the in-memory map.
4. If no match is found and fallback is enabled, it walks up to the parent cell at resolution 4.
5. Returns `null`/`None` if no match exists.

## SDKs

| Language | Package | Docs |
|---|---|---|
| JavaScript / TypeScript | [`@aialok/lakhua`](https://www.npmjs.com/package/@aialok/lakhua) | [libs/javascript](./libs/javascript/README.md) |
| Python | [`lakhua`](https://pypi.org/project/lakhua/) | [libs/python](./libs/python/README.md) |
| Go | [`github.com/aialok/lakhua/libs/go`](https://pkg.go.dev/github.com/aialok/lakhua/libs/go) | [libs/go](./libs/go/README.md) |

Each SDK has identical behavior and option signatures.

## Install

### JavaScript / TypeScript

```bash
npm install @aialok/lakhua
# or
bun add @aialok/lakhua
```

### Python

```bash
pip install lakhua
```

### Go

```bash
go get github.com/aialok/lakhua/libs/go
```

## Minimal Usage

### JavaScript / TypeScript

```ts
import { geocode } from "@aialok/lakhua";

const result = geocode(28.6139, 77.2090);
if (result) {
  console.log(result.city, result.state);
}
```

### Python

```python
from lakhua import geocode

result = geocode(28.6139, 77.2090)
if result:
    print(result.city, result.state)
```

### Go

```go
result := lakhua.Geocode(28.6139, 77.2090, nil)
if result != nil {
    fmt.Println(result.City, result.State)
}
```

## Options

All SDKs accept the same options:

| Option | Type | Default | Description |
|---|---|---|---|
| `resolution` | int | `5` | H3 resolution used for `geocode(lat, lon)` |
| `fallback` | bool | `true` | Walk up to parent resolution if no match |
| `debug` | bool | `false` | Print load and lookup timing logs |

## Data Coverage

The dataset covers major Indian cities and districts using H3 resolutions 4 and 5.  
Coverage is not exhaustive — rural or remote areas may return `null`.

## Contributing

Issues and PRs are welcome.  
If you find a location that returns incorrect or missing results, open an issue with the coordinates.

See each SDK's `README.md` for local development setup.

## Project Status

Active. JavaScript, Python, and Go SDKs are implemented and tested.

## License

MIT
