import { SUPPORTED_RESOLUTIONS, readReverseGeoStore } from "../config/constants.js";
import type { ReverseGeoStore } from "../types/geocode.js";

/**
 * Singleton loader that preloads all configured reverse-geo stores into memory once.
 */
export class ReverseGeoDataLoader {
  private static instance: ReverseGeoDataLoader | null = null;
  private readonly stores = new Map<number, ReverseGeoStore>();
  private isLoaded = false;
  private testOverride: Partial<Record<number, ReverseGeoStore>> | null = null;

  private constructor() {}

  /** Returns the singleton loader instance. */
  static getInstance(): ReverseGeoDataLoader {
    if (!ReverseGeoDataLoader.instance) {
      ReverseGeoDataLoader.instance = new ReverseGeoDataLoader();
    }
    return ReverseGeoDataLoader.instance;
  }

  private loadAllStoresOnce(debug = false): void {
    if (this.isLoaded) {
      return;
    }

    const startedAt = performance.now();
    for (const resolution of SUPPORTED_RESOLUTIONS) {
      this.stores.set(resolution, readReverseGeoStore(resolution));
    }
    this.isLoaded = true;

    if (debug) {
      const elapsedMs = performance.now() - startedAt;
      console.log(`[lakhua][debug] loaded all stores into memory in ${elapsedMs.toFixed(3)}ms`);
    }
  }

  /**
   * Returns the store for the requested resolution.
   * Loads all stores once on first call.
   */
  loadResolutionStore(resolution: number, debug = false): ReverseGeoStore {
    const override = this.testOverride?.[resolution];
    if (override) {
      if (debug) {
        console.log(`[lakhua][debug] using test override store for r${resolution}`);
      }
      return override;
    }

    this.loadAllStoresOnce(debug);

    const startedAt = performance.now();
    const store = this.stores.get(resolution) ?? {};
    if (debug) {
      const elapsedMs = performance.now() - startedAt;
      console.log(
        `[lakhua][debug] fetched in-memory store r${resolution} in ${elapsedMs.toFixed(3)}ms`,
      );
    }
    return store;
  }

  /** Sets temporary in-memory test stores by resolution. */
  setStoresForTesting(stores: Partial<Record<number, ReverseGeoStore>> | null): void {
    this.testOverride = stores;
  }

  /** Clears preloaded stores; next lookup reloads from disk. */
  clearStoreCache(): void {
    this.stores.clear();
    this.isLoaded = false;
  }
}

/** Shared singleton instance used by the default geocoder. */
export const defaultDataLoader = ReverseGeoDataLoader.getInstance();
