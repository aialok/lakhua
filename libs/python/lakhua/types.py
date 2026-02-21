"""
Data types used throughout lakhua for geocoding operations.

These dataclasses define the structure of location results and options you can
pass to geocoding functions.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class GeocodeResult:
    """
    Complete result from a geocoding lookup, including match metadata.

    This is the main data structure returned by geocode() and geocode_h3(),
    containing location details (city, state, etc.) plus metadata about which
    H3 cell was matched and at what resolution.
    """

    city: str
    """Name of the city or town."""

    state: str
    """Name of the state or union territory."""

    matched_h3: str
    """
    The H3 cell ID that was found in the database.

    This may be the exact H3 cell for your input coordinates, or a parent cell
    if fallback was used to find a match at a lower resolution.
    """

    matched_resolution: int
    """
    The H3 resolution level where the match was found.

    Resolution 5 (default) provides city-level accuracy (~73 km² cells).
    Resolution 4 provides state/region-level accuracy (~410 km² cells).
    """

    district: Optional[str] = None
    """District name, when available in the dataset."""

    pincode: Optional[str] = None
    """Postal code (PIN code), when available in the dataset."""


# Kept for backward compatibility, but GeocodeResult is the main type
LocationDetails = GeocodeResult


@dataclass
class GeocodeOptions:
    """
    Configuration options for controlling geocoding behavior.

    Use these options to tune how lakhua performs lookups, including the precision
    level and whether to fall back to coarser resolutions when exact matches fail.
    """

    resolution: int = 5
    """
    H3 resolution to use when converting coordinates to H3 cells.

    Higher resolutions (5) give finer geographic detail but may have less data coverage.
    Lower resolutions (4) cover larger areas and have broader coverage.
    Default is 5 for city-level accuracy.
    """

    fallback: bool = True
    """
    Whether to check parent H3 cells if the exact cell has no data.

    When True (default), if your coordinates don't match any data at resolution 5,
    lakhua automatically checks the parent cell at resolution 4. This increases
    the chance of finding a match, though at lower geographic precision.
    """

    debug: bool = False
    """
    Enable debug logging to see timing information for data loading and lookups.

    When True, lakhua prints messages showing how long it took to load data from
    disk and how long each lookup operation takes. Useful for performance analysis.
    """


# Type alias for internal data storage
ReverseGeoStore = Dict[str, Dict[str, str]]
"""
Internal type representing the in-memory geographic database.

Maps H3 cell IDs (strings) to location information (dictionaries with city, state, etc.).
You typically don't need to work with this type directly.
"""

