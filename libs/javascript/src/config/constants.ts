import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import type { ReverseGeoStore } from "../types/geocode.js";

/** Minimum supported H3 resolution for lookup. */
export const MIN_RESOLUTION = 4;
/** Maximum supported H3 resolution for lookup. */
export const MAX_RESOLUTION = 5;
/** Default H3 resolution used for `geocode(lat, lon)` conversion. */
export const DEFAULT_RESOLUTION = MAX_RESOLUTION;
/** Preloaded resolution set, loaded once into in-memory stores. */
export const SUPPORTED_RESOLUTIONS = [4, 5] as const;

/** Relative folder name where reverse geo JSON files are stored. */
export const DATA_DIR_NAME = "data";
/** Prefix used by reverse geo data files: `reverse_geo_{resolution}.json`. */
export const DATA_FILE_PREFIX = "reverse_geo_";

/**
 * Returns the absolute path for a reverse geo data file for a resolution.
 */
export function getDataFilePath(resolution: number): string {
  const currentDir = dirname(fileURLToPath(import.meta.url));
  return join(currentDir, "..", "..", DATA_DIR_NAME, `${DATA_FILE_PREFIX}${resolution}.json`);
}

/**
 * Reads and parses a reverse geo store for a resolution.
 * Returns an empty store when the file does not exist.
 */
export function readReverseGeoStore(resolution: number): ReverseGeoStore {
  const filePath = getDataFilePath(resolution);
  if (!existsSync(filePath)) {
    return {};
  }

  const raw = readFileSync(filePath, "utf-8");
  return JSON.parse(raw) as ReverseGeoStore;
}
