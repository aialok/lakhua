"""
Core reverse geocoding engine for lakhua.

This module implements the main geocoding logic, converting coordinates or H3 cells
into location information. Most users should use the top-level geocode() and
geocode_h3() functions rather than interacting with this module directly.
"""

import time
from typing import Optional

import h3

from lakhua.core.constants import DEFAULT_RESOLUTION, MAX_RESOLUTION, MIN_RESOLUTION
from lakhua.core.data_loader import DataLoader, default_data_loader
from lakhua.types import GeocodeOptions, GeocodeResult


def _clamp_resolution(resolution: int) -> int:
    """
    Internal utility to ensure resolution values stay within supported bounds.

    If you request a resolution outside the 4-5 range, the library automatically
    adjusts it to the nearest supported value rather than failing.

    Args:
        resolution: Requested H3 resolution.

    Returns:
        Valid resolution between 4 and 5.
    """
    if not isinstance(resolution, int):
        return DEFAULT_RESOLUTION
    if resolution < MIN_RESOLUTION:
        return MIN_RESOLUTION
    if resolution > MAX_RESOLUTION:
        return MAX_RESOLUTION
    return resolution


class ReverseGeocoder:
    """
    Converts coordinates and H3 cells into location information for India.

    This is the core geocoding engine. For most use cases, you should use the
    simpler top-level geocode() and geocode_h3() functions instead of creating
    instances of this class directly.

    The geocoder automatically handles:
    - Loading data from disk into memory on first use
    - Falling back to parent H3 cells when exact matches aren't found
    - Validating input coordinates and H3 indices

    Example (advanced usage):
        >>> geocoder = ReverseGeocoder.get_instance()
        >>> result = geocoder.geocode(28.6139, 77.2090)
    """

    _instance: Optional["ReverseGeocoder"] = None
    _data_loader: DataLoader

    def __new__(cls, data_loader: Optional[DataLoader] = None) -> "ReverseGeocoder":
        """
        Internal constructor ensuring only one geocoder exists per process.

        This singleton pattern means all geocoding operations share the same
        in-memory data and configuration, keeping memory usage efficient.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data_loader = data_loader or default_data_loader
        return cls._instance

    @classmethod
    def get_instance(cls) -> "ReverseGeocoder":
        """
        Get the shared geocoder instance.

        You rarely need to call this directly. Use the top-level geocode() and
        geocode_h3() functions instead, which use this instance automatically.

        Returns:
            The shared ReverseGeocoder instance used by all geocoding operations.
        """
        return cls()

    def geocode_h3(
        self,
        h3_index: str,
        options: Optional[GeocodeOptions] = None,
    ) -> Optional[GeocodeResult]:
        """
        Convert an H3 cell ID into location information (city, state, etc.).

        When you have an H3 cell ID (perhaps from spatial indexing or another system),
        this method looks it up in lakhua's India location database. If the exact cell
        isn't found and fallback is enabled (default), it automatically checks parent
        cells at lower resolutions until a match is found or all options are exhausted.

        Args:
            h3_index: H3 cell index string (e.g., "8560145bfffffff").
            options: Optional settings to control resolution and fallback behavior.

        Returns:
            Location details including city, state, and the matched H3 cell, or None
            if the H3 index is invalid or no location data exists for that area.

        Example:
            >>> result = geocoder.geocode_h3("8560145bfffffff")
            >>> if result:
            ...     print(f"{result.city}, {result.state}")
        """
        opts = options or GeocodeOptions()

        if not h3.is_valid_cell(h3_index):
            if opts.debug:
                print("[lakhua][debug] invalid h3 index provided")
            return None

        start_time = time.perf_counter()
        input_resolution = h3.get_resolution(h3_index)
        start_resolution = _clamp_resolution(input_resolution)
        end_resolution = MIN_RESOLUTION if opts.fallback else start_resolution

        for resolution in range(start_resolution, end_resolution - 1, -1):
            candidate = (
                h3_index
                if resolution == input_resolution
                else h3.cell_to_parent(h3_index, resolution)
            )
            store = self._data_loader.load_resolution_store(resolution, opts.debug)

            lookup_start = time.perf_counter()
            match = store.get(candidate)
            if opts.debug:
                lookup_elapsed_ms = (time.perf_counter() - lookup_start) * 1000
                print(
                    "[lakhua][debug] lookup key "
                    f"{candidate} in r{resolution} took {lookup_elapsed_ms:.3f}ms"
                )

            if match:
                if opts.debug:
                    total_elapsed_ms = (time.perf_counter() - start_time) * 1000
                    print(f"[lakhua][debug] match found in {total_elapsed_ms:.3f}ms")
                return GeocodeResult(
                    city=match.get("city", ""),
                    state=match.get("state", ""),
                    district=match.get("district"),
                    pincode=match.get("pincode"),
                    matched_h3=candidate,
                    matched_resolution=resolution,
                )

        if opts.debug:
            total_elapsed_ms = (time.perf_counter() - start_time) * 1000
            print(f"[lakhua][debug] no match found in {total_elapsed_ms:.3f}ms")

        return None

    def geocode(
        self,
        lat: float,
        lon: float,
        options: Optional[GeocodeOptions] = None,
    ) -> Optional[GeocodeResult]:
        """
        Convert latitude/longitude coordinates into location information.

        This is the most common way to use lakhua. Pass in any coordinates within
        India, and get back the city, state, and other location details. The library
        first converts your coordinates to an H3 cell, then looks up that cell in
        the location database.

        Args:
            lat: Latitude in decimal degrees (-90 to 90).
            lon: Longitude in decimal degrees (-180 to 180).
            options: Optional settings to control resolution and fallback behavior.

        Returns:
            Location details including city, state, and the matched H3 cell, or None
            if coordinates are invalid or no location data exists for that area.

        Example:
            >>> result = geocoder.geocode(28.6139, 77.2090)
            >>> if result:
            ...     print(f"Found: {result.city}, {result.state}")
        """
        opts = options or GeocodeOptions()

        if not (isinstance(lat, (int, float)) and isinstance(lon, (int, float))):
            return None
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return None

        resolution = _clamp_resolution(opts.resolution)
        h3_index = h3.latlng_to_cell(lat, lon, resolution)
        return self.geocode_h3(h3_index, opts)


# Default geocoder instance used by the top-level geocode() and geocode_h3() functions
default_geocoder = ReverseGeocoder.get_instance()

