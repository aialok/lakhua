"""
lakhua: Fast, offline reverse geocoding for India.

This library provides in-memory reverse geocoding using H3 spatial indexing.
"""

from typing import Optional

from lakhua.core import (
    DATA_DIR_NAME,
    DATA_FILE_PREFIX,
    DEFAULT_RESOLUTION,
    MAX_RESOLUTION,
    MIN_RESOLUTION,
    SUPPORTED_RESOLUTIONS,
    DataLoader,
    ReverseGeocoder,
    default_data_loader,
    default_geocoder,
)
from lakhua.types import GeocodeOptions, GeocodeResult, LocationDetails

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "DATA_DIR_NAME",
    "DATA_FILE_PREFIX",
    "DEFAULT_RESOLUTION",
    "MAX_RESOLUTION",
    "MIN_RESOLUTION",
    "SUPPORTED_RESOLUTIONS",
    "DataLoader",
    "ReverseGeocoder",
    "default_data_loader",
    "default_geocoder",
    "GeocodeOptions",
    "GeocodeResult",
    "LocationDetails",
    "geocode",
    "geocode_h3",
]


def geocode(
    lat: float,
    lon: float,
    options: Optional[GeocodeOptions] = None,
) -> Optional[GeocodeResult]:
    """
    Reverse geocodes latitude/longitude into India location metadata.

    Uses the library's internal singleton geocoder, so you can call this directly
    without creating any class instance.

    Args:
        lat: Latitude in decimal degrees.
        lon: Longitude in decimal degrees.
        options: Lookup options such as fallback and debug logging.

    Returns:
        Matched location details, or None when input is invalid / no match exists.

    Example:
        >>> from lakhua import geocode
        >>> result = geocode(28.6139, 77.2090)
        >>> print(result.city, result.state)
    """
    return default_geocoder.geocode(lat, lon, options)


def geocode_h3(
    h3_index: str,
    options: Optional[GeocodeOptions] = None,
) -> Optional[GeocodeResult]:
    """
    Reverse geocodes an H3 cell index directly.

    Uses the library's internal singleton geocoder. When fallback is enabled
    (default), parent resolutions are checked until the minimum supported resolution.

    Args:
        h3_index: H3 cell index string.
        options: Lookup options such as fallback and debug logging.

    Returns:
        Matched location details, or None when input is invalid / no match exists.

    Example:
        >>> from lakhua import geocode_h3
        >>> result = geocode_h3("8560145bfffffff")
        >>> print(result.city if result else "No match")
    """
    return default_geocoder.geocode_h3(h3_index, options)

