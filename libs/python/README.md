# lakhua (Python)

Offline reverse geocoding for India, optimized for fast in-memory lookups using H3 indexes.

## Features

- **Offline-first**: No API keys, no network dependency
- **In-memory lookup**: Singleton loader for efficient data management
- **Parent-resolution fallback**: Automatic fallback from resolution 5 → 4
- **Type-safe**: Full type hints and dataclasses
- **Modern Python**: Supports Python 3.8+
- **Fast**: In-memory map-based lookups with minimal overhead

## Installation

```bash
pip install lakhua
```

## Quick Start

```python
from lakhua import geocode

location = geocode(28.6139, 77.209)

if location:
    print(location.city, location.state)
```

## API Reference

### Recommended top-level APIs

- `geocode(lat, lon, options=None) -> GeocodeResult | None`
- `geocode_h3(h3_index, options=None) -> GeocodeResult | None`

These helpers use the default singleton geocoder internally.

### Advanced class APIs

- `ReverseGeocoder.get_instance()`
- `DataLoader.get_instance()`

Use these only when you need explicit control in advanced runtime or testing scenarios.

### `GeocodeOptions`

```python
@dataclass
class GeocodeOptions:
    resolution: int = 5        # H3 resolution for geocode(lat, lon)
    fallback: bool = True      # Enable parent resolution fallback
    debug: bool = False        # Print timing logs
```

### `GeocodeResult`

```python
@dataclass
class GeocodeResult:
    city: str
    state: str
    district: str | None
    pincode: str | None
    matched_h3: str
    matched_resolution: int
```

Returns `None` for invalid inputs or when no match is found.

## Examples

### Coordinate lookup

```python
from lakhua import geocode

result = geocode(12.9716, 77.5946)
print(result)
```

### Direct H3 lookup

```python
from lakhua import geocode_h3

result = geocode_h3("8560145bfffffff")
print(result)
```

### Debug mode

```python
from lakhua import geocode, GeocodeOptions

result = geocode(19.076, 72.8777, GeocodeOptions(debug=True))
print(result)
```

### Custom resolution

```python
from lakhua import geocode, GeocodeOptions

result = geocode(
    28.6139, 77.2090,
    GeocodeOptions(resolution=4, fallback=False)
)
```

## Performance Notes

- Data files are loaded once per process into memory
- Lookups are map-based in-memory operations
- Fallback adds up to two additional parent checks (5 → 4) when enabled
- Average lookup time: < 1ms (in-memory)

## Project Layout

```text
lakhua/
  core/
    __init__.py
    constants.py
    data_loader.py
    geocoder.py
  types.py
  __init__.py
  data/
    reverse_geo_4.json
    reverse_geo_5.json
```

## Development

### Setup

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

### Linting and formatting

```bash
ruff check .
ruff format .
```

### Type checking

```bash
mypy lakhua
```

## License

MIT

