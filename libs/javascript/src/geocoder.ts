import { cellToParent, getResolution, isValidCell, latLngToCell } from "h3-js";
import { defaultDataLoader, type ReverseGeoDataLoader } from "./dataLoader.js";
import { DEFAULT_RESOLUTION, MAX_RESOLUTION, MIN_RESOLUTION } from "./contant.js";
import type { GeocodeOptions, GeocodeResult } from "./types.js";

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

export class ReverseGeocoder {
  private static instance: ReverseGeocoder | null = null;
  private constructor(private readonly dataLoader: ReverseGeoDataLoader = defaultDataLoader) { }

  static getInstance(): ReverseGeocoder {
    if (!ReverseGeocoder.instance) {
      ReverseGeocoder.instance = new ReverseGeocoder();
    }
    return ReverseGeocoder.instance;
  }

  geocodeH3(h3Index: string, options: GeocodeOptions = {}): GeocodeResult | null {
    if (!isValidCell(h3Index)) {
      return null;
    }

    const fallback = options.fallback ?? true;
    const startResolution = clampResolution(getResolution(h3Index));
    const endResolution = fallback ? MIN_RESOLUTION : startResolution;

    for (let resolution = startResolution; resolution >= endResolution; resolution -= 1) {
      const candidate =
        resolution === startResolution ? h3Index : cellToParent(h3Index, resolution);
      const match = this.dataLoader.loadResolutionStore(resolution)[candidate];
      if (match) {
        return {
          ...match,
          matched_h3: candidate,
          matched_resolution: resolution,
        };
      }
    }

    return null;
  }

  geocode(lat: number, lon: number, options: GeocodeOptions = {}): GeocodeResult | null {
    if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
      return null;
    }

    const resolution = clampResolution(options.resolution ?? DEFAULT_RESOLUTION);
    const h3Index = latLngToCell(lat, lon, resolution);
    return this.geocodeH3(h3Index, options);
  }
}

export const defaultGeocoder = ReverseGeocoder.getInstance();

