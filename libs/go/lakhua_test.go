package lakhua

import (
	"testing"

	h3 "github.com/uber/h3-go/v3"
)

func boolOption(v bool) *bool {
	return &v
}

func setupTestStores() {
	GetDataLoader().SetStoresForTesting(
		map[int]map[string]LocationDetails{
			5: {
				"8560145bfffffff": {
					City:  "New Delhi",
					State: "Delhi",
				},
			},
			4: {
				"8460145ffffffff": {
					City:  "Delhi Region",
					State: "Delhi",
				},
			},
		},
	)
}

func teardownTestStores() {
	GetDataLoader().SetStoresForTesting(nil)
	GetDataLoader().ClearStoreCache()
}

func TestGeocodeH3ExactMatch(t *testing.T) {
	setupTestStores()
	defer teardownTestStores()

	result := GeocodeH3("8560145bfffffff", nil)
	if result == nil {
		t.Fatal("expected non-nil result")
	}
	if result.City != "New Delhi" || result.State != "Delhi" {
		t.Fatalf("unexpected result: %+v", result)
	}
	if result.MatchedResolution != 5 {
		t.Fatalf("expected matched resolution 5, got %d", result.MatchedResolution)
	}
}

func TestGeocodeH3Fallback(t *testing.T) {
	setupTestStores()
	defer teardownTestStores()

	parent := h3.FromString("8460145ffffffff")
	children := h3.ToChildren(parent, 5)
	var sibling string
	for _, child := range children {
		childStr := h3.ToString(child)
		if childStr != "8560145bfffffff" {
			sibling = childStr
			break
		}
	}
	if sibling == "" {
		t.Fatal("failed to find sibling cell")
	}

	result := GeocodeH3(sibling, nil)
	if result == nil {
		t.Fatal("expected fallback match")
	}
	if result.MatchedResolution != 4 {
		t.Fatalf("expected fallback resolution 4, got %d", result.MatchedResolution)
	}
}

func TestGeocodeH3NoFallback(t *testing.T) {
	setupTestStores()
	defer teardownTestStores()

	parent := h3.FromString("8460145ffffffff")
	children := h3.ToChildren(parent, 5)
	var sibling string
	for _, child := range children {
		childStr := h3.ToString(child)
		if childStr != "8560145bfffffff" {
			sibling = childStr
			break
		}
	}
	result := GeocodeH3(sibling, &GeocodeOptions{Fallback: boolOption(false)})
	if result != nil {
		t.Fatalf("expected nil without fallback, got %+v", result)
	}
}

func TestGeocodeH3Invalid(t *testing.T) {
	result := GeocodeH3("invalid", nil)
	if result != nil {
		t.Fatalf("expected nil for invalid index, got %+v", result)
	}
}

func TestGeocodeCoordinatesValidation(t *testing.T) {
	if Geocode(999, 999, nil) != nil {
		t.Fatal("expected nil for invalid coordinates")
	}
}
