# Architecture

`lakhua` provides offline reverse geocoding for India using precomputed H3-indexed datasets.

## High-level flow

1. Caller provides `lat/lon` or an `h3Index`.
2. For `lat/lon`, the SDK converts coordinates to H3 at configured resolution (default `5`).
3. SDK looks up the H3 key in an in-memory store.
4. If no exact match and fallback enabled, SDK checks parent resolution (`5 -> 4`).
5. Returns location metadata or empty result.

## Data model

- Files: `reverse_geo_4.json`, `reverse_geo_5.json`
- Key: H3 cell id string
- Value:
  - `city` (required)
  - `state` (required)
  - `district` (optional)
  - `pincode` (optional)

## Runtime design

- Data is loaded once per process (singleton loader pattern).
- Query path is synchronous and memory-only after first load.
- Debug mode prints load and lookup timing.
- No outbound network calls.

## SDK layout

- JavaScript: `libs/javascript/src`
  - `core/geocoder.ts` lookup logic
  - `core/data-loader.ts` cache + loading
  - `config/constants.ts` resolutions and file access
- Python: `libs/python/lakhua/core`
  - `geocoder.py` lookup logic
  - `data_loader.py` cache + loading
  - `constants.py` resolutions and file access
- Go: `libs/go`
  - `lakhua.go` public API + lookup orchestration
  - `internal/loader/loader.go` cache + loading
  - `internal/config/constants.go` resolutions and file access

## Cross-language contract

All SDKs intentionally share:

- Default resolution: `5`
- Supported lookup resolutions: `4`, `5`
- Fallback default: enabled
- Output fields: city/state + optional district/pincode + matched H3 metadata

## Build data pipeline

Tools under `tools/` generate reverse-geo JSON files from OSM-derived inputs.
Generated artifacts are copied into SDK data directories for packaging.

