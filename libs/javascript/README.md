# lakhua

Offline reverse geocoding for India, optimized for fast in-memory lookups using H3 indexes.

## Features

- offline-first (no API keys, no network dependency)
- in-memory lookup with singleton loader
- parent-resolution fallback (`5 -> 4`)
- Bun-native tooling (test, lint, format)
- TypeScript-first API with full type definitions

## Installation

```bash
bun add @aialok/lakhua
# or
npm install @aialok/lakhua
```

## Quick Start

```ts
import { geocode } from "@aialok/lakhua";

const location = geocode(28.6139, 77.209);

if (location) {
  console.log(location.city, location.state);
}
```

## API Reference

### Recommended top-level APIs

- `geocode(lat, lon, options?) => GeocodeResult | null`
- `geocodeH3(h3Index, options?) => GeocodeResult | null`

These helpers use the default singleton geocoder internally.

### Advanced class APIs

- `ReverseGeocoder.getInstance()`
- `ReverseGeoDataLoader.getInstance()`

Use these only when you need explicit control in advanced runtime or testing scenarios.

### `GeocodeOptions`

- `resolution?: number`  
  H3 resolution used during `geocode(lat, lon)`. Default is `5`.
- `fallback?: boolean`  
  Default `true`. If enabled, lookup tries parent resolutions until `4`.
- `debug?: boolean`  
  Enables internal timing logs for loading and in-memory key lookups.

### `GeocodeResult`

```ts
interface GeocodeResult {
  city: string;
  state: string;
  district?: string;
  pincode?: string;
  matched_h3: string;
  matched_resolution: number;
}
```

Returns `null` for invalid inputs or when no match is found.

## Examples

### Coordinate lookup

```ts
import { geocode } from "@aialok/lakhua";

const result = geocode(12.9716, 77.5946);
console.log(result);
```

### Direct H3 lookup

```ts
import { geocodeH3 } from "@aialok/lakhua";

const result = geocodeH3("866189b1fffffff");
console.log(result);
```

### Debug mode

```ts
import { geocode } from "@aialok/lakhua";

const result = geocode(19.076, 72.8777, { debug: true });
console.log(result);
```

## Performance Notes

- Data files are loaded once per process into memory.
- Lookups are map-based in-memory operations.
- Fallback adds up to two additional parent checks (`5`, `4`) when enabled.

## Project Layout

```text
src/
  core/
    geocoder.ts
    data-loader.ts
  config/
    constants.ts
  types/
    geocode.ts
  index.ts
```

Compatibility re-exports are still available:

- `src/geocoder.ts`
- `src/dataLoader.ts`
- `src/types.ts`
- `src/contant.ts`

## Development

```bash
bun run lint
bun run format
bun run typecheck
bun test
```
