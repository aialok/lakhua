import { cellToParent, getResolution, isValidCell, latLngToCell } from "h3-js";
import { DEFAULT_RESOLUTION, MAX_RESOLUTION, MIN_RESOLUTION } from "../config/constants.js";
import type { GeocodeOptions, GeocodeResult } from "../types/geocode.js";
import { type ReverseGeoDataLoader, defaultDataLoader } from "./data-loader.js";

function clampResolution(resolution: number): number {
  if (!Number.isInteger(resolution)) {
    return DEFAULT_RESOLUTION;
  }
  if (resolution < MIN_RESOLUTION) {
    return MIN_RESOLUTION;
  }
  if (resolution > MAX_RESOLUTION) {
    return MAX_RESOLUTION;
  }
  return resolution;
}

/**
 * Main geocoder service for offline reverse geocoding.
 *
 * Most users should call top-level `geocode()` / `geocodeH3()` exports.
 * Use this class directly when you need explicit control in advanced scenarios.
 */
export class ReverseGeocoder {
  private static instance: ReverseGeocoder | null = null;
  private constructor(private readonly dataLoader: ReverseGeoDataLoader = defaultDataLoader) {}

  /**
   * Returns the shared singleton geocoder instance.
   */
  static getInstance(): ReverseGeocoder {
    if (!ReverseGeocoder.instance) {
      ReverseGeocoder.instance = new ReverseGeocoder();
    }
    return ReverseGeocoder.instance;
  }

  /**
   * Resolves an H3 index to location metadata.
   *
   * If `fallback` is enabled (default), the lookup attempts:
   * `currentResolution -> parentResolution ... -> MIN_RESOLUTION`.
   *
   * @param h3Index H3 cell index.
   * @param options Lookup options.
   * @returns Matched location details, or `null` when no match exists.
   */
  geocodeH3(h3Index: string, options: GeocodeOptions = {}): GeocodeResult | null {
    if (!isValidCell(h3Index)) {
      if (options.debug) {
        console.log("[lakhua][debug] invalid h3 index provided");
      }
      return null;
    }

    const startedAt = performance.now();
    const debug = options.debug ?? false;
    const fallback = options.fallback ?? true;
    const inputResolution = getResolution(h3Index);
    const startResolution = clampResolution(inputResolution);
    const endResolution = fallback ? MIN_RESOLUTION : startResolution;

    for (let resolution = startResolution; resolution >= endResolution; resolution -= 1) {
      const candidate =
        resolution === inputResolution ? h3Index : cellToParent(h3Index, resolution);
      const store = this.dataLoader.loadResolutionStore(resolution, debug);

      const lookupStartAt = performance.now();
      const match = store[candidate];
      if (debug) {
        const lookupElapsedMs = performance.now() - lookupStartAt;
        console.log(
          `[lakhua][debug] lookup key ${candidate} in r${resolution} took ${lookupElapsedMs.toFixed(3)}ms`,
        );
      }

      if (match) {
        if (debug) {
          const totalElapsedMs = performance.now() - startedAt;
          console.log(`[lakhua][debug] match found in ${totalElapsedMs.toFixed(3)}ms`);
        }
        return {
          ...match,
          matched_h3: candidate,
          matched_resolution: resolution,
        };
      }
    }

    if (debug) {
      const totalElapsedMs = performance.now() - startedAt;
      console.log(`[lakhua][debug] no match found in ${totalElapsedMs.toFixed(3)}ms`);
    }

    return null;
  }

  /**
   * Resolves geographic coordinates to location metadata.
   *
   * Coordinates are converted to H3 using `options.resolution` (default `5`),
   * then resolved using the same fallback rules as `geocodeH3`.
   *
   * @param lat Latitude in decimal degrees.
   * @param lon Longitude in decimal degrees.
   * @param options Lookup options.
   * @returns Matched location details, or `null` when no match exists.
   */
  geocode(lat: number, lon: number, options: GeocodeOptions = {}): GeocodeResult | null {
    if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
      return null;
    }
    if (lat < -90 || lat > 90 || lon < -180 || lon > 180) {
      return null;
    }

    const resolution = clampResolution(options.resolution ?? DEFAULT_RESOLUTION);
    const h3Index = latLngToCell(lat, lon, resolution);
    return this.geocodeH3(h3Index, options);
  }
}

/** Shared singleton geocoder instance used by top-level helper functions. */
export const defaultGeocoder = ReverseGeocoder.getInstance();
