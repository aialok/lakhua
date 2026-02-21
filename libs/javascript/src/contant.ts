import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import type { ReverseGeoStore } from "./types.js";

export const MIN_RESOLUTION = 4;
export const MAX_RESOLUTION = 6;
export const DEFAULT_RESOLUTION = MAX_RESOLUTION;
export const SUPPORTED_RESOLUTIONS = [4, 5, 6] as const;

export const DATA_DIR_NAME = "data";
export const DATA_FILE_PREFIX = "reverse_geo_";

export function getDataFilePath(resolution: number): string {
  const currentDir = dirname(fileURLToPath(import.meta.url));
  return join(currentDir, "..", DATA_DIR_NAME, `${DATA_FILE_PREFIX}${resolution}.json`);
}

export function readReverseGeoStore(resolution: number): ReverseGeoStore {
  const filePath = getDataFilePath(resolution);
  if (!existsSync(filePath)) {
    return {};
  }

  const raw = readFileSync(filePath, "utf-8");
  return JSON.parse(raw) as ReverseGeoStore;
}

