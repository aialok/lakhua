# FAQ

## Is `lakhua` online or offline?

Offline. The SDK loads local JSON data into memory and performs in-process lookups.

## Does it support countries outside India?

No. Current datasets target India only.

## Why can some coordinates return no result?

Coverage is not exhaustive. If no matching cell exists (including fallback parent lookup), SDKs return `null`/`None`/`nil`.

## What is fallback?

When enabled (default), lookup tries exact resolution first (typically `5`) and then parent resolution (`4`) if needed.

## Is the first call slower?

Usually yes. First call reads data files into memory. Later calls are memory lookups and are much faster.

## Can I use H3 directly?

Yes. Use:

- JavaScript: `geocodeH3(h3Index)`
- Python: `geocode_h3(h3_index)`
- Go: `GeocodeH3(h3Index, options)`

## Is this suitable for production?

Yes for India-focused, low-latency reverse geocoding use cases where city/state-level results are acceptable.

## How do I debug lookup behavior?

Enable debug in options:

- JavaScript: `{ debug: true }`
- Python: `GeocodeOptions(debug=True)`
- Go: `&lakhua.GeocodeOptions{Debug: true}`

