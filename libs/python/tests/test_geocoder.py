"""Unit tests for lakhua geocoder."""

import h3
import pytest

from lakhua import DataLoader, GeocodeOptions, ReverseGeocoder, geocode, geocode_h3


def _get_sibling_cell(cell_5: str) -> str:
    """Return a valid resolution-5 sibling cell that shares the same resolution-4 parent."""
    parent_cell_4 = h3.cell_to_parent(cell_5, 4)
    siblings = h3.cell_to_children(parent_cell_4, 5)
    return next(cell for cell in siblings if cell != cell_5)


@pytest.fixture
def test_data_loader():
    """Fixture providing a data loader with test data."""
    loader = DataLoader.get_instance()

    # Use real H3 parent-child relationship
    test_cell_5 = "8560145bfffffff"
    parent_cell_4 = h3.cell_to_parent(test_cell_5, 4)  # Compute actual parent

    loader.set_stores_for_testing(
        {
            5: {
                test_cell_5: {
                    "city": "New Delhi",
                    "state": "Delhi",
                    "district": "Central Delhi",
                    "pincode": "110001",
                }
            },
            4: {
                parent_cell_4: {
                    "city": "Delhi Region",
                    "state": "Delhi",
                }
            },
        }
    )
    yield loader
    loader.set_stores_for_testing(None)
    loader.clear_store_cache()


def test_geocode_h3_exact_match(test_data_loader):
    """Test direct H3 index lookup with exact match."""
    result = geocode_h3("8560145bfffffff")
    assert result is not None
    assert result.city == "New Delhi"
    assert result.state == "Delhi"
    assert result.district == "Central Delhi"
    assert result.pincode == "110001"
    assert result.matched_h3 == "8560145bfffffff"
    assert result.matched_resolution == 5


def test_geocode_h3_fallback(test_data_loader):
    """Test H3 lookup with parent fallback."""
    test_cell_5 = "8560145bfffffff"
    parent_cell_4 = h3.cell_to_parent(test_cell_5, 4)
    sibling_cell = _get_sibling_cell(test_cell_5)

    result = geocode_h3(sibling_cell)
    assert result is not None
    assert result.city == "Delhi Region"
    assert result.state == "Delhi"
    assert result.matched_h3 == parent_cell_4
    assert result.matched_resolution == 4


def test_geocode_h3_no_fallback(test_data_loader):
    """Test H3 lookup with fallback disabled."""
    sibling_cell = _get_sibling_cell("8560145bfffffff")
    result = geocode_h3(
        sibling_cell,  # Not in res 5 data, would fallback to res 4 if enabled
        GeocodeOptions(fallback=False)
    )
    assert result is None


def test_geocode_h3_invalid_index():
    """Test H3 lookup with invalid index."""
    result = geocode_h3("invalid_h3_index")
    assert result is None


def test_geocode_h3_no_match(test_data_loader):
    """Test H3 lookup with no matching data."""
    result = geocode_h3("8660145bfffffff")  # Different region
    assert result is None


def test_geocode_coordinates(test_data_loader):
    """Test coordinate-based geocoding."""
    # Coordinates roughly in Delhi region
    result = geocode(28.6139, 77.2090)
    # Result depends on actual H3 conversion, just check it doesn't crash
    assert result is None or isinstance(result.city, str)


def test_geocode_invalid_coordinates():
    """Test geocoding with invalid coordinates."""
    assert geocode(999, 999) is None
    assert geocode("invalid", 77.0) is None  # type: ignore


def test_geocode_with_options(test_data_loader):
    """Test geocoding with custom options."""
    result = geocode(
        28.6139,
        77.2090,
        GeocodeOptions(resolution=5, fallback=True, debug=False)
    )
    # Just verify it doesn't crash with options
    assert result is None or result.city


def test_singleton_pattern():
    """Test that geocoder and data loader are singletons."""
    geocoder1 = ReverseGeocoder.get_instance()
    geocoder2 = ReverseGeocoder.get_instance()
    assert geocoder1 is geocoder2

    loader1 = DataLoader.get_instance()
    loader2 = DataLoader.get_instance()
    assert loader1 is loader2


def test_geocode_options_defaults():
    """Test GeocodeOptions default values."""
    opts = GeocodeOptions()
    assert opts.resolution == 5
    assert opts.fallback is True
    assert opts.debug is False


def test_geocode_result_structure(test_data_loader):
    """Test GeocodeResult has all expected fields."""
    result = geocode_h3("8560145bfffffff")
    assert result is not None
    assert hasattr(result, "city")
    assert hasattr(result, "state")
    assert hasattr(result, "district")
    assert hasattr(result, "pincode")
    assert hasattr(result, "matched_h3")
    assert hasattr(result, "matched_resolution")

