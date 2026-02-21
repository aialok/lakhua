# lakhua (Go)

Sub-millisecond reverse geocoding for India. Runs entirely in-memory — zero API calls, zero network, zero latency overhead.

[![Go](https://img.shields.io/badge/go-pkg.go.dev-blue)](https://pkg.go.dev/github.com/aialok/lakhua/libs/go)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](../../LICENSE)

## Features

- 📍 converts `lat, lon` to `City`, `State`, optional `District` and `Pincode`
- 🔢 supports direct H3 index lookup via `GeocodeH3()`
- ↩️ parent-cell fallback (`resolution 5 → 4`) when exact cell has no data
- ⚡ data loaded once per process using `sync.Once` — all subsequent lookups are in-memory map reads
- 🐛 optional debug mode traces load time and per-lookup timing

## Installation

```bash
go get github.com/aialok/lakhua/libs/go
```

> The geographic data files are bundled with the module — nothing to configure manually.

## Quick Start

```go
package main

import (
    "fmt"

    lakhua "github.com/aialok/lakhua/libs/go"
)

func main() {
    result := lakhua.Geocode(28.6139, 77.2090, nil)
    if result != nil {
        fmt.Println(result.City, result.State)
    }
}
```

## API

### Top-level functions (recommended)

```go
func Geocode(lat, lon float64, options *GeocodeOptions) *GeocodeResult
func GeocodeH3(h3Index string, options *GeocodeOptions) *GeocodeResult
```

These use the internal singleton geocoder — no struct instantiation needed.

### `GeocodeOptions`

```go
type GeocodeOptions struct {
    Resolution int   // H3 resolution for Geocode(lat, lon). Default: 5
    Fallback   *bool // Walk up to parent resolution on miss. Default: true
    Debug      bool  // Print load and lookup timings. Default: false
}
```

Pass `nil` to use all defaults.

### `GeocodeResult`

```go
type GeocodeResult struct {
    City              string
    State             string
    District          *string // nil if not available
    Pincode           *string // nil if not available
    MatchedH3         string  // H3 cell that matched (may be parent)
    MatchedResolution int     // Resolution of the matched cell
}
```

Returns `nil` for invalid input or when no data exists for the given location.

### Advanced singleton access

```go
func GetGeocoder() *ReverseGeocoder
func GetDataLoader() *ReverseGeoDataLoader
```

Use these only when you need explicit control — e.g. testing or custom lifecycle management.

## Examples

### Coordinate lookup

```go
result := lakhua.Geocode(12.9716, 77.5946, nil) // Bengaluru
if result != nil {
    fmt.Println(result.City, result.State)
}
```

### Direct H3 lookup

```go
result := lakhua.GeocodeH3("8560145bfffffff", nil)
if result != nil {
    fmt.Println(result.City)
}
```

### Debug mode

```go
result := lakhua.Geocode(19.076, 72.8777, &lakhua.GeocodeOptions{
    Debug: true,
})
// prints load + lookup timings to stdout
```

### Disable fallback

```go
noFallback := false
result := lakhua.Geocode(28.6139, 77.2090, &lakhua.GeocodeOptions{
    Fallback: &noFallback,
})
// only checks resolution 5, no parent lookup
```

## Performance

- Data is loaded into memory once on first call (using `sync.Once`).
- Each lookup is a single map read — typically < 1ms.
- With fallback enabled, up to 2 map reads (resolution 5, then 4).

## Development

```bash
go test ./...
go vet ./...
```

## License

MIT
