import { defaultGeocoder } from "./core/geocoder.js";

export { ReverseGeocoder, defaultGeocoder } from "./core/geocoder.js";
export { ReverseGeoDataLoader, defaultDataLoader } from "./core/data-loader.js";
export {
  DATA_DIR_NAME,
  DATA_FILE_PREFIX,
  DEFAULT_RESOLUTION,
  MAX_RESOLUTION,
  MIN_RESOLUTION,
  SUPPORTED_RESOLUTIONS,
} from "./config/constants.js";
export type {
  GeocodeOptions,
  GeocodeResult,
  LocationDetails,
  ReverseGeoStore,
} from "./types/geocode.js";

/**
 * Reverse geocodes latitude/longitude into India location metadata.
 *
 * Uses the library's internal singleton geocoder, so you can call this directly
 * without creating any class instance.
 *
 * @param lat Latitude in decimal degrees.
 * @param lon Longitude in decimal degrees.
 * @param options Lookup options such as fallback and debug logging.
 * @returns Matched location details, or `null` when input is invalid / no match exists.
 *
 * @example
 * ```ts
 * import { geocode } from "lakhua";
 * const result = geocode(28.6139, 77.2090);
 * ```
 */
export function geocode(
  lat: number,
  lon: number,
  options?: import("./types/geocode.js").GeocodeOptions,
): import("./types/geocode.js").GeocodeResult | null {
  return defaultGeocoder.geocode(lat, lon, options);
}

/**
 * Reverse geocodes an H3 cell index directly.
 *
 * Uses the library's internal singleton geocoder. When fallback is enabled
 * (default), parent resolutions are checked until the minimum supported resolution.
 *
 * @param h3Index H3 cell index string.
 * @param options Lookup options such as fallback and debug logging.
 * @returns Matched location details, or `null` when input is invalid / no match exists.
 *
 * @example
 * ```ts
 * import { geocodeH3 } from "lakhua";
 * const result = geocodeH3("866189b1fffffff");
 * ```
 */
export function geocodeH3(
  h3Index: string,
  options?: import("./types/geocode.js").GeocodeOptions,
): import("./types/geocode.js").GeocodeResult | null {
  return defaultGeocoder.geocodeH3(h3Index, options);
}
