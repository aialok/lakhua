# lakhua (Go)

Offline reverse geocoding for India, optimized for fast in-memory lookups using H3 indexes.

## Features

- Offline-first (no API keys, no network dependency)
- In-memory lookup with singleton loader
- Parent-resolution fallback (`5 -> 4`)
- Debug timings for load and lookup paths

## Installation

```bash
go get github.com/aialok/lakhua/libs/go
```

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

- `Geocode(lat, lon float64, options *GeocodeOptions) *GeocodeResult`
- `GeocodeH3(h3Index string, options *GeocodeOptions) *GeocodeResult`
- `GetGeocoder() *ReverseGeocoder`
- `GetDataLoader() *ReverseGeoDataLoader`

## Options

```go
type GeocodeOptions struct {
    Resolution int   // default: 5
    Fallback   *bool // default: true
    Debug      bool  // default: false
}
```

## Data files

The library expects the following files under `libs/go/data`:

- `reverse_geo_4.json`
- `reverse_geo_5.json`

## Development

```bash
go test ./...
```

