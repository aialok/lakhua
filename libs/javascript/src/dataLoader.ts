import { readReverseGeoStore, SUPPORTED_RESOLUTIONS } from "./contant.js";
import type { ReverseGeoStore } from "./types.js";

export class ReverseGeoDataLoader {
  private static instance: ReverseGeoDataLoader | null = null;
  private readonly stores = new Map<number, ReverseGeoStore>();
  private isLoaded = false;
  private testOverride: Partial<Record<number, ReverseGeoStore>> | null = null;

  private constructor() {}

  static getInstance(): ReverseGeoDataLoader {
    if (!ReverseGeoDataLoader.instance) {
      ReverseGeoDataLoader.instance = new ReverseGeoDataLoader();
    }
    return ReverseGeoDataLoader.instance;
  }

  private loadAllStoresOnce(): void {
    if (this.isLoaded) {
      return;
    }

    for (const resolution of SUPPORTED_RESOLUTIONS) {
      this.stores.set(resolution, readReverseGeoStore(resolution));
    }
    this.isLoaded = true;
  }

  loadResolutionStore(resolution: number): ReverseGeoStore {
    const override = this.testOverride?.[resolution];
    if (override) {
      return override;
    }

    this.loadAllStoresOnce();
    return this.stores.get(resolution) ?? {};
  }

  setStoresForTesting(stores: Partial<Record<number, ReverseGeoStore>> | null): void {
    this.testOverride = stores;
  }

  clearStoreCache(): void {
    this.stores.clear();
    this.isLoaded = false;
  }
}

export const defaultDataLoader = ReverseGeoDataLoader.getInstance();

