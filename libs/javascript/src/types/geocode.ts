/** Normalized location details associated with an H3 cell. */
export interface LocationDetails {
  city: string;
  state: string;
  district?: string;
  pincode?: string;
}

/** In-memory reverse geo store keyed by H3 index. */
export type ReverseGeoStore = Record<string, LocationDetails>;

/** Successful geocode result with match metadata. */
export interface GeocodeResult extends LocationDetails {
  matched_h3: string;
  matched_resolution: number;
}

/** Options to tune lookup behavior for `geocode` and `geocodeH3`. */
export interface GeocodeOptions {
  /** H3 resolution for coordinate conversion in `geocode(lat, lon)`. Default is `5`. */
  resolution?: number;
  /** Enables parent fallback lookup from current resolution down to `4`. Default is `true`. */
  fallback?: boolean;
  /** Prints timing logs for initial load and per-lookup access. */
  debug?: boolean;
}
