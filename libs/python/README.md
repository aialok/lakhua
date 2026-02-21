# lakhua (Python)

Sub-millisecond reverse geocoding for India. Runs entirely in-memory — zero API calls, zero network, zero latency overhead.

[![PyPI](https://img.shields.io/pypi/v/lakhua)](https://pypi.org/project/lakhua/)
[![Python](https://img.shields.io/pypi/pyversions/lakhua)](https://pypi.org/project/lakhua/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](../../LICENSE)

## Features

- 📍 converts `lat, lon` to `city`, `state`, optional `district` and `pincode`
- 🔢 supports direct H3 index lookup via `geocode_h3()`
- ↩️ parent-cell fallback (`resolution 5 → 4`) when exact cell has no data
- ⚡ data loaded once per process — all subsequent lookups are in-memory dict reads
- 🐛 optional debug mode traces load time and per-lookup timing
- 🔷 fully typed — dataclasses with `py.typed` marker included

## Installation

```bash
pip install lakhua
```

## Quick Start

```python
from lakhua import geocode

result = geocode(28.6139, 77.2090)
if result:
    print(result.city, result.state)
```

## API

### Top-level functions (recommended)

```python
geocode(lat: float, lon: float, options: Optional[GeocodeOptions] = None) -> Optional[GeocodeResult]
geocode_h3(h3_index: str, options: Optional[GeocodeOptions] = None) -> Optional[GeocodeResult]
```

These use the internal singleton geocoder — no class instantiation needed.

### `GeocodeOptions`

```python
from dataclasses import dataclass

@dataclass
class GeocodeOptions:
    resolution: int = 5       # H3 resolution for geocode(lat, lon)
    fallback: bool = True     # Walk up to parent resolution on miss
    debug: bool = False       # Print load and lookup timings
```

### `GeocodeResult`

```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class GeocodeResult:
    city: str
    state: str
    matched_h3: str            # H3 cell that matched (may be parent)
    matched_resolution: int    # Resolution of the matched cell
    district: Optional[str] = None
    pincode: Optional[str] = None
```

Returns `None` for invalid input or when no data exists for the given location.

### Advanced class APIs

```python
from lakhua import ReverseGeocoder, DataLoader

ReverseGeocoder.get_instance()
DataLoader.get_instance()
```

Use these only when you need explicit control — e.g. testing or custom singleton lifecycle.

## Examples

### Coordinate lookup

```python
from lakhua import geocode

result = geocode(12.9716, 77.5946)  # Bengaluru
if result:
    print(result.city, result.state, result.pincode)
```

### Direct H3 lookup

```python
from lakhua import geocode_h3

result = geocode_h3("8560145bfffffff")
if result:
    print(result.city)
```

### Debug mode

```python
from lakhua import geocode, GeocodeOptions

result = geocode(19.076, 72.8777, GeocodeOptions(debug=True))
# prints load + lookup timings to stdout
```

### Disable fallback

```python
from lakhua import geocode, GeocodeOptions

result = geocode(28.6139, 77.2090, GeocodeOptions(fallback=False))
# only checks resolution 5, no parent lookup
```

## Performance

- Data is loaded into memory once on first call.
- Each lookup is a single dict read — typically < 1ms.
- With fallback enabled, up to 2 dict reads (resolution 5, then 4).

## Development

```bash
# install with dev dependencies
pip install -e ".[dev]"

# run tests
pytest

# lint and format
ruff check .
ruff format .

# type check
mypy lakhua
```

## License

MIT
