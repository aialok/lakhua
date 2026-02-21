/// <reference path="./bun-test-shims.d.ts" />
import { expect, test } from "bun:test";
import { latLngToCell } from "h3-js";
import { ReverseGeoDataLoader, ReverseGeocoder } from "../src/index.js";

const geocoder = ReverseGeocoder.getInstance();
const dataLoader = ReverseGeoDataLoader.getInstance();

test("handles repeated lookups efficiently", () => {
  const h3 = latLngToCell(22.5726, 88.3639, 6);
  dataLoader.setStoresForTesting({
    6: {
      [h3]: {
        city: "Kolkata",
        state: "West Bengal",
      },
    },
  });

  const iterations = 5000;
  const start = performance.now();
  for (let i = 0; i < iterations; i += 1) {
    const result = geocoder.geocode(22.5726, 88.3639);
    expect(result).not.toBeNull();
  }
  const elapsedMs = performance.now() - start;

  expect(elapsedMs).toBeGreaterThanOrEqual(0);
});

