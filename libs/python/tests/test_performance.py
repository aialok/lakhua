"""Performance tests for lakhua geocoder."""

import time

import pytest

from lakhua import DataLoader, GeocodeOptions, geocode_h3


@pytest.fixture
def test_data_loader():
    """Fixture providing a data loader with test data."""
    loader = DataLoader.get_instance()
    loader.set_stores_for_testing(
        {
            5: {
                f"856014{i:x}fffffff": {
                    "city": f"City{i}",
                    "state": "TestState",
                }
                for i in range(100)
            }
        }
    )
    yield loader
    loader.set_stores_for_testing(None)
    loader.clear_store_cache()


def test_geocode_h3_performance(test_data_loader):
    """Test H3 lookup performance."""
    iterations = 1000
    start = time.perf_counter()

    for i in range(iterations):
        geocode_h3(f"856014{i % 100:x}fffffff")

    elapsed = time.perf_counter() - start
    avg_ms = (elapsed / iterations) * 1000

    print(f"\nAverage H3 lookup time: {avg_ms:.3f}ms")
    assert avg_ms < 1.0, "H3 lookup should be under 1ms on average"


def test_data_load_performance():
    """Test data loading performance."""
    loader = DataLoader.get_instance()
    loader.clear_store_cache()

    start = time.perf_counter()
    loader.load_resolution_store(5, debug=False)
    elapsed = time.perf_counter() - start

    print(f"\nData load time: {elapsed * 1000:.3f}ms")
    # This will vary based on data size, just ensure it completes
    assert elapsed < 5.0, "Data load should complete within 5 seconds"


def test_fallback_performance(test_data_loader):
    """Test performance with fallback enabled."""
    iterations = 100
    start = time.perf_counter()

    for _ in range(iterations):
        geocode_h3("8560140000fffff", GeocodeOptions(fallback=True))

    elapsed = time.perf_counter() - start
    avg_ms = (elapsed / iterations) * 1000

    print(f"\nAverage fallback lookup time: {avg_ms:.3f}ms")
    assert avg_ms < 2.0, "Fallback lookup should be under 2ms on average"

