export interface LocationDetails {
  city: string;
  state: string;
  district?: string;
  pincode?: string;
}

export type ReverseGeoStore = Record<string, LocationDetails>;

export interface GeocodeResult extends LocationDetails {
  matched_h3: string;
  matched_resolution: number;
}

export interface GeocodeOptions {
  resolution?: number;
  fallback?: boolean;
}

