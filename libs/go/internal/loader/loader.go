package loader

import (
	"fmt"
	"sync"
	"time"

	"github.com/aialok/lakhua/libs/go/internal/config"
)

type DataLoader struct {
	once         sync.Once
	stores       map[int]config.ReverseGeoStore
	testOverride map[int]config.ReverseGeoStore
	mu           sync.RWMutex
}

var (
	defaultLoader     *DataLoader
	defaultLoaderOnce sync.Once
)

func GetDefault() *DataLoader {
	defaultLoaderOnce.Do(func() {
		defaultLoader = &DataLoader{
			stores: make(map[int]config.ReverseGeoStore),
		}
	})
	return defaultLoader
}

func (l *DataLoader) loadAllStoresOnce(debug bool) {
	l.once.Do(func() {
		startedAt := time.Now()
		for _, resolution := range config.SupportedResolutions {
			l.stores[resolution] = config.ReadReverseGeoStore(resolution)
		}
		if debug {
			fmt.Printf("[lakhua][debug] loaded all stores into memory in %.3fms\n", time.Since(startedAt).Seconds()*1000)
		}
	})
}

func (l *DataLoader) LoadResolutionStore(resolution int, debug bool) config.ReverseGeoStore {
	l.mu.RLock()
	override, ok := l.testOverride[resolution]
	l.mu.RUnlock()
	if ok {
		if debug {
			fmt.Printf("[lakhua][debug] using test override store for r%d\n", resolution)
		}
		return override
	}

	l.loadAllStoresOnce(debug)

	startedAt := time.Now()
	store := l.stores[resolution]
	if store == nil {
		store = config.ReverseGeoStore{}
	}
	if debug {
		fmt.Printf("[lakhua][debug] fetched in-memory store r%d in %.3fms\n", resolution, time.Since(startedAt).Seconds()*1000)
	}
	return store
}

func (l *DataLoader) SetStoresForTesting(stores map[int]config.ReverseGeoStore) {
	l.mu.Lock()
	defer l.mu.Unlock()
	l.testOverride = stores
}

func (l *DataLoader) ClearStoreCache() {
	l.mu.Lock()
	defer l.mu.Unlock()
	l.stores = make(map[int]config.ReverseGeoStore)
	l.once = sync.Once{}
}
