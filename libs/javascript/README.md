# @aialok/lakhua

Sub-millisecond reverse geocoding for India. Runs entirely in-memory — zero API calls, zero network, zero latency overhead.

[![npm](https://img.shields.io/npm/v/@aialok/lakhua)](https://www.npmjs.com/package/@aialok/lakhua)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](../../LICENSE)

## Features

- 📍 converts `lat, lon` to `city`, `state`, optional `district` and `pincode`
- 🔢 supports direct H3 index lookup via `geocodeH3()`
- ↩️ parent-cell fallback (`resolution 5 → 4`) when exact cell has no data
- ⚡ data loaded once per process — all subsequent lookups are in-memory map reads
- 🐛 optional debug mode traces load time and per-lookup timing
- 🔷 TypeScript-first — full type definitions included

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

## Performance

- Data is loaded into memory once on first call.
- Each lookup is a single map read — typically < 1ms.
- With fallback enabled, up to 2 map reads (resolution 5, then 4).

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
