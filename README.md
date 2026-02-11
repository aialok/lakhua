# Lakhua

Fast, offline reverse geocoding for India. No API keys, no costs.

Named after my hometown, a small town barely on most maps.

## Install

```bash
pip install lakhua
npm install lakhua
go get github.com/aialok/lakhua
```

## Use

```python
from lakhua import geocode

location = geocode(28.6139, 77.2090)
print(location['city'])  # New Delhi
```

## License

MIT