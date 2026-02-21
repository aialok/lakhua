/// <reference path="./bun-test-shims.d.ts" />
import { beforeEach, expect, test } from "bun:test";
import { cellToParent, latLngToCell } from "h3-js";
import { ReverseGeoDataLoader, ReverseGeocoder } from "../src/index.js";

const geocoder = ReverseGeocoder.getInstance();
const dataLoader = ReverseGeoDataLoader.getInstance();

beforeEach(() => {
  dataLoader.setStoresForTesting(null);
});

test("returns exact match for geocodeH3", () => {
  const h3 = latLngToCell(28.6139, 77.209, 5);

  dataLoader.setStoresForTesting({
    5: {
      [h3]: {
        city: "New Delhi",
        state: "Delhi",
      },
    },
  });

  const result = geocoder.geocodeH3(h3);
  expect(result).not.toBeNull();
  expect(result?.city).toBe("New Delhi");
  expect(result?.state).toBe("Delhi");
  expect(result?.matched_h3).toBe(h3);
  expect(result?.matched_resolution).toBe(5);
});

test("falls back to parent resolution when exact match is missing", () => {
  const h3Res5 = latLngToCell(28.6139, 77.209, 5);
  const h3Res4 = cellToParent(h3Res5, 4);

  dataLoader.setStoresForTesting({
    5: {
      [h3Res5]: {
        city: "Delhi",
        state: "Delhi",
      },
    },
    4: {
      [h3Res4]: {
        city: "India",
        state: "India",
      },
    },
  });

  const result = geocoder.geocodeH3(h3Res5);
  expect(result).not.toBeNull();
  expect(result?.city).toBe("Delhi");
  expect(result?.matched_h3).toBe(h3Res5);
  expect(result?.matched_resolution).toBe(5);
});

test("returns null when not found", () => {
  dataLoader.setStoresForTesting({
    5: {},
    4: {},
  });

  const h3 = latLngToCell(19.076, 72.8777, 5);
  const result = geocoder.geocodeH3(h3);
  expect(result).toBeNull();
});

test("geocode() converts coordinates and resolves", () => {
  const h3 = latLngToCell(12.9716, 77.5946, 5);
  dataLoader.setStoresForTesting({
    5: {
      [h3]: {
        city: "Bengaluru",
        state: "Karnataka",
      },
    },
  });

  const result = geocoder.geocode(12.9716, 77.5946);
  expect(result).not.toBeNull();
  expect(result?.city).toBe("Bengaluru");
  expect(result?.matched_resolution).toBe(5);
});
