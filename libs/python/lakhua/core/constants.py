"""
Configuration constants for lakhua reverse geocoding.

This module defines resolution ranges and data file paths used by the library.
You typically don't need to import these directly unless you're building custom
geocoding logic or need to understand the library's resolution constraints.
"""

import json
from pathlib import Path
from typing import Dict, cast

# Resolution configuration
MIN_RESOLUTION: int = 4
"""
Minimum H3 resolution supported by lakhua.

Lower resolutions cover larger geographic areas. Resolution 4 cells are roughly
410 km² each, providing country/state-level granularity.
"""

MAX_RESOLUTION: int = 5
"""
Maximum H3 resolution supported by lakhua.

Higher resolutions provide finer geographic detail. Resolution 5 cells are roughly
73 km² each, suitable for city-level accuracy.
"""

DEFAULT_RESOLUTION: int = MAX_RESOLUTION
"""
Default H3 resolution used when you call geocode(lat, lon) without specifying a resolution.

Set to resolution 5 for city-level accuracy by default. You can override this by
passing GeocodeOptions(resolution=4) to geocode().
"""

SUPPORTED_RESOLUTIONS: tuple[int, ...] = (4, 5)
"""
H3 resolutions preloaded into memory when the library initializes.

The library loads data for these resolutions once on first use, enabling fast
in-memory lookups without repeated disk I/O.
"""

# Data file configuration
DATA_DIR_NAME: str = "data"
"""Directory name where reverse geocoding data files are stored within the package."""

DATA_FILE_PREFIX: str = "reverse_geo_"
"""Filename prefix for data files. Full names follow the pattern: reverse_geo_{resolution}.json"""


def get_data_file_path(resolution: int) -> Path:
    """
    Internal utility to locate data files for a given H3 resolution.

    You don't need to call this directly. The library uses it internally to
    load geographic data when geocode() or geocode_h3() is first called.

    Args:
        resolution: H3 resolution level (4 or 5).

    Returns:
        Path to the JSON data file for that resolution.
    """
    current_dir = Path(__file__).parent
    return current_dir.parent / DATA_DIR_NAME / f"{DATA_FILE_PREFIX}{resolution}.json"


def read_reverse_geo_store(resolution: int) -> Dict[str, Dict[str, str]]:
    """
    Internal utility to load and parse geographic data for a resolution.

    You don't need to call this directly. The DataLoader uses it automatically
    when loading data into memory. Returns an empty dictionary if the data file
    doesn't exist, allowing the library to gracefully handle missing data.

    Args:
        resolution: H3 resolution level (4 or 5).

    Returns:
        Dictionary mapping H3 cell IDs to location metadata (city, state, etc.).
    """
    file_path = get_data_file_path(resolution)
    if not file_path.exists():
        return {}

    with open(file_path, encoding="utf-8") as f:
        return cast(Dict[str, Dict[str, str]], json.load(f))

