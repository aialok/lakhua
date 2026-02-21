"""
Data loading infrastructure for lakhua reverse geocoding.

This module handles loading geographic data from disk into memory. The library
automatically loads data once when you first call geocode() or geocode_h3(),
so you typically don't need to interact with this module directly.
"""

import time
from typing import Dict, Optional

from lakhua.core.constants import SUPPORTED_RESOLUTIONS, read_reverse_geo_store
from lakhua.types import ReverseGeoStore


class DataLoader:
    """
    Manages loading and caching of geographic data in memory.

    The DataLoader ensures data is loaded only once per process, making subsequent
    geocoding lookups extremely fast. You don't need to create instances of this
    class yourself — the library provides a default instance that's used automatically.

    For most use cases, simply call geocode() or geocode_h3() and the data loading
    happens transparently in the background.
    """

    _instance: Optional["DataLoader"] = None
    _stores: Dict[int, ReverseGeoStore]
    _is_loaded: bool
    _test_override: Optional[Dict[int, ReverseGeoStore]]

    def __new__(cls) -> "DataLoader":
        """
        Internal constructor ensuring only one DataLoader exists per process.

        This singleton pattern means all geocoding operations share the same
        in-memory data, avoiding redundant loads and keeping memory usage efficient.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._stores = {}
            cls._instance._is_loaded = False
            cls._instance._test_override = None
        return cls._instance

    @classmethod
    def get_instance(cls) -> "DataLoader":
        """
        Get the shared data loader instance.

        You rarely need to call this directly. Use the top-level geocode() and
        geocode_h3() functions instead, which use this loader automatically.

        Returns:
            The shared DataLoader instance used by all geocoding operations.
        """
        return cls()

    def _load_all_stores_once(self, debug: bool = False) -> None:
        """
        Internal method that loads geographic data into memory on first use.

        This happens automatically the first time you call geocode() or geocode_h3().
        Subsequent calls reuse the in-memory data for fast lookups.

        Args:
            debug: When True, prints timing information showing how long data loading took.
        """
        if self._is_loaded:
            return

        start_time = time.perf_counter()
        for resolution in SUPPORTED_RESOLUTIONS:
            self._stores[resolution] = read_reverse_geo_store(resolution)
        self._is_loaded = True

        if debug:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            print(f"[lakhua][debug] loaded all stores into memory in {elapsed_ms:.3f}ms")

    def load_resolution_store(self, resolution: int, debug: bool = False) -> ReverseGeoStore:
        """
        Get geographic data for a specific H3 resolution.

        This method loads data from disk into memory on first call, then returns
        cached data on subsequent calls. You typically don't call this directly —
        the ReverseGeocoder uses it internally during lookups.

        Args:
            resolution: H3 resolution level (4 or 5).
            debug: When True, prints timing information for data access.

        Returns:
            Dictionary mapping H3 cell IDs to location information (city, state, etc.).
        """
        if self._test_override and resolution in self._test_override:
            if debug:
                print(f"[lakhua][debug] using test override store for r{resolution}")
            return self._test_override[resolution]

        self._load_all_stores_once(debug)

        start_time = time.perf_counter()
        store = self._stores.get(resolution, {})
        if debug:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            print(f"[lakhua][debug] fetched in-memory store r{resolution} in {elapsed_ms:.3f}ms")
        return store

    def set_stores_for_testing(self, stores: Optional[Dict[int, ReverseGeoStore]]) -> None:
        """
        Override data with custom test data (for testing purposes only).

        Useful when writing unit tests for code that uses lakhua, allowing you
        to inject controlled test data instead of loading real geographic data.

        Args:
            stores: Dictionary mapping resolution numbers to test data, or None to clear overrides.
        """
        self._test_override = stores

    def clear_store_cache(self) -> None:
        """
        Force reload of data from disk on next lookup.

        Clears the in-memory cache, causing the next geocode() call to reload
        data from disk. Useful if you've updated data files and want to pick up
        changes without restarting your application.
        """
        self._stores.clear()
        self._is_loaded = False


# Default data loader instance used by geocode() and geocode_h3()
default_data_loader = DataLoader.get_instance()

