# @aialok/lakhua

Sub-millisecond reverse geocoding for India, fully offline.

No API calls. No network latency. No rate limits.

Built for backend services, cron jobs, and analytics workloads that need deterministic geocode lookups.

[![npm](https://img.shields.io/npm/v/@aialok/lakhua)](https://www.npmjs.com/package/@aialok/lakhua)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](../../LICENSE)

## Features

- 📍 converts `lat, lon` to `city`, `state`, optional `district` and `pincode`
- 🔢 supports direct H3 index lookup via `geocodeH3()`
- ↩️ parent-cell fallback (`resolution 5 → 4`) when exact cell has no data
- ⚡ data loaded once per process — all subsequent lookups are in-memory map reads
- 🐛 optional debug mode traces load time and per-lookup timing
- 🔷 TypeScript-first — full type definitions included

## Why Not Hosted APIs?

| Feature | `@aialok/lakhua` | Hosted API |
|---|---|---|
| Works offline | yes | no |
| API key required | no | usually yes |
| Network dependency | no | yes |
| Per-request cost | no | usually yes |
| Latency variability | low, in-process | network-dependent |

## Installation

```bash
npm install @aialok/lakhua
# or
bun add @aialok/lakhua
```

## Quick Start

```ts
import { geocode } from "@aialok/lakhua";

const result = geocode(28.6139, 77.2090);
if (result) {
  console.log(result.city, result.state);
}
```

## API

### Top-level functions (recommended)

```ts
geocode(lat: number, lon: number, options?: GeocodeOptions): GeocodeResult | null
geocodeH3(h3Index: string, options?: GeocodeOptions): GeocodeResult | null
```

These use the internal singleton geocoder — no class instantiation needed.

### `GeocodeOptions`

```ts
interface GeocodeOptions {
  resolution?: number;  // H3 resolution for geocode(lat, lon). Default: 5
  fallback?: boolean;   // Walk up to parent resolution on miss. Default: true
  debug?: boolean;      // Print load and lookup timings. Default: false
}
```

### `GeocodeResult`

```ts
interface GeocodeResult {
  city: string;
  state: string;
  district?: string;
  pincode?: string;
  matched_h3: string;         // H3 cell that matched (may be parent)
  matched_resolution: number; // Resolution of the matched cell
}
```

Returns `null` for invalid input or when no data exists for the given location.

### Advanced class APIs

```ts
import { ReverseGeocoder, ReverseGeoDataLoader } from "@aialok/lakhua";

ReverseGeocoder.getInstance()
ReverseGeoDataLoader.getInstance()
```

Use these only when you need explicit control — e.g. testing or custom singleton lifecycle.

## Examples

### Coordinate lookup

```ts
import { geocode } from "@aialok/lakhua";

const result = geocode(12.9716, 77.5946); // Bengaluru
if (result) {
  console.log(result.city, result.state, result.pincode);
}
```

### Direct H3 lookup

```ts
import { geocodeH3 } from "@aialok/lakhua";

const result = geocodeH3("8560145bfffffff");
if (result) {
  console.log(result.city);
}
```

### Debug mode

```ts
import { geocode } from "@aialok/lakhua";

const result = geocode(19.076, 72.8777, { debug: true });
// prints load + lookup timings to console
```

### Disable fallback

```ts
import { geocode } from "@aialok/lakhua";

const result = geocode(28.6139, 77.2090, { fallback: false });
// only checks resolution 5, no parent lookup
```

## How It Works

1. Convert `lat, lon` to H3 at resolution 5 (or configured resolution).
2. Lookup the H3 key in in-memory store.
3. If not found and fallback is enabled, check parent resolution 4.
4. Return a result object, or `null` if no match exists.

```text
lat, lon -> h3(res5) -> in-memory map -> optional parent(res4) -> result/null
```

## Data Source and Indexing

- Indexing system: [Uber H3](https://h3geo.org/)
- Geographic source data: OpenStreetMap data by [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)
- Distribution model: precomputed JSON stores bundled with the package

## Data Coverage

- India-focused dataset
- H3 resolutions: 4 and 5
- Fields: `city`, `state`
- Optional fields: `district`, `pincode` (when available)

## Runtime Compatibility

- Node.js
- Bun

`@aialok/lakhua` reads packaged JSON files from local filesystem at runtime.

## Performance

- Data is loaded into memory once on first call.
- Each lookup is a single map read — typically < 1ms.
- With fallback enabled, up to 2 map reads (resolution 5, then 4).

## Benchmarking

Use `test/performance.test.ts` to benchmark in your own environment.
When publishing numbers, include machine type, runtime version, and warm/cold process context.

## When Not To Use

- You need rooftop-level precision
- You need global coverage
- You need live POI or continuously updated location feeds

## Development

```bash
bun install
bun run lint
bun run format
bun run typecheck
bun test
```

## License

MIT
