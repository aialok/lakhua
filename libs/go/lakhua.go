// Package lakhua provides fast, offline reverse geocoding for India using H3.
// Keywords: reverse geocoding, offline geocoding, india geocoding, geocoding,
// geospatial, GIS, H3, H3 index, OpenStreetMap, OSM, point in polygon, bounding
// box, admin boundaries, geospatial indexing, coordinates, latitude, longitude,
// city, state, district, tehsil, postal code, pincode, batch geocoding, location
// lookup, no api key, free geocoding, india maps.
package lakhua

import (
	"fmt"
	"math"
	"sync"
	"time"

	"github.com/aialok/lakhua/libs/go/internal/config"
	"github.com/aialok/lakhua/libs/go/internal/loader"
	h3 "github.com/uber/h3-go/v3"
)

type LocationDetails struct {
	City     string  `json:"city"`
	State    string  `json:"state"`
	District *string `json:"district,omitempty"`
	Pincode  *string `json:"pincode,omitempty"`
}

type GeocodeResult struct {
	LocationDetails
	MatchedH3         string `json:"matched_h3"`
	MatchedResolution int    `json:"matched_resolution"`
}

type GeocodeOptions struct {
	Resolution int
	Fallback   *bool
	Debug      bool
}

type ReverseGeoDataLoader struct {
	impl *loader.DataLoader
}

type ReverseGeocoder struct {
	dataLoader *ReverseGeoDataLoader
}

var (
	defaultDataLoaderOnce sync.Once
	defaultDataLoader     *ReverseGeoDataLoader
	defaultGeocoderOnce   sync.Once
	defaultGeocoder       *ReverseGeocoder
)

func GetDataLoader() *ReverseGeoDataLoader {
	defaultDataLoaderOnce.Do(func() {
		defaultDataLoader = &ReverseGeoDataLoader{impl: loader.GetDefault()}
	})
	return defaultDataLoader
}

func GetGeocoder() *ReverseGeocoder {
	defaultGeocoderOnce.Do(func() {
		defaultGeocoder = &ReverseGeocoder{dataLoader: GetDataLoader()}
	})
	return defaultGeocoder
}

func Geocode(lat float64, lon float64, options *GeocodeOptions) *GeocodeResult {
	return GetGeocoder().Geocode(lat, lon, options)
}

func GeocodeH3(h3Index string, options *GeocodeOptions) *GeocodeResult {
	return GetGeocoder().GeocodeH3(h3Index, options)
}

func (d *ReverseGeoDataLoader) SetStoresForTesting(stores map[int]map[string]LocationDetails) {
	converted := make(map[int]config.ReverseGeoStore)
	for res, store := range stores {
		convertedStore := make(config.ReverseGeoStore)
		for key, value := range store {
			convertedStore[key] = config.LocationDetails{
				City:     value.City,
				State:    value.State,
				District: value.District,
				Pincode:  value.Pincode,
			}
		}
		converted[res] = convertedStore
	}
	d.impl.SetStoresForTesting(converted)
}

func (d *ReverseGeoDataLoader) ClearStoreCache() {
	d.impl.ClearStoreCache()
}

func (g *ReverseGeocoder) GeocodeH3(h3Index string, options *GeocodeOptions) *GeocodeResult {
	opts := normalizeOptions(options)
	index := h3.FromString(h3Index)
	if !h3.IsValid(index) {
		if opts.Debug {
			fmt.Println("[lakhua][debug] invalid h3 index provided")
		}
		return nil
	}

	startedAt := time.Now()
	inputResolution := h3.Resolution(index)
	startResolution := config.ClampResolution(inputResolution)
	endResolution := startResolution
	if fallbackEnabled(opts) {
		endResolution = config.MinResolution
	}

	for resolution := startResolution; resolution >= endResolution; resolution-- {
		candidate := index
		if resolution != inputResolution {
			candidate = h3.ToParent(index, resolution)
		}
		candidateString := h3.ToString(candidate)
		store := g.dataLoader.impl.LoadResolutionStore(resolution, opts.Debug)

		lookupStartedAt := time.Now()
		match, ok := store[candidateString]
		if opts.Debug {
			fmt.Printf("[lakhua][debug] lookup key %s in r%d took %.3fms\n", candidateString, resolution, time.Since(lookupStartedAt).Seconds()*1000)
		}

		if ok {
			if opts.Debug {
				fmt.Printf("[lakhua][debug] match found in %.3fms\n", time.Since(startedAt).Seconds()*1000)
			}
			return &GeocodeResult{
				LocationDetails: LocationDetails{
					City:     match.City,
					State:    match.State,
					District: match.District,
					Pincode:  match.Pincode,
				},
				MatchedH3:         candidateString,
				MatchedResolution: resolution,
			}
		}
	}

	if opts.Debug {
		fmt.Printf("[lakhua][debug] no match found in %.3fms\n", time.Since(startedAt).Seconds()*1000)
	}
	return nil
}

func (g *ReverseGeocoder) Geocode(lat float64, lon float64, options *GeocodeOptions) *GeocodeResult {
	if math.IsNaN(lat) || math.IsNaN(lon) || math.IsInf(lat, 0) || math.IsInf(lon, 0) {
		return nil
	}
	if lat < -90 || lat > 90 || lon < -180 || lon > 180 {
		return nil
	}

	opts := normalizeOptions(options)
	resolution := opts.Resolution
	index := h3.FromGeo(h3.GeoCoord{Latitude: lat, Longitude: lon}, resolution)
	return g.GeocodeH3(h3.ToString(index), opts)
}

func normalizeOptions(options *GeocodeOptions) *GeocodeOptions {
	if options == nil {
		return &GeocodeOptions{
			Resolution: config.DefaultResolution,
			Fallback:   boolPtr(true),
			Debug:      false,
		}
	}

	resolution := options.Resolution
	if resolution == 0 {
		resolution = config.DefaultResolution
	}
	resolution = config.ClampResolution(resolution)

	var fallback *bool
	if options.Fallback == nil {
		fallback = boolPtr(true)
	} else {
		fallback = options.Fallback
	}

	return &GeocodeOptions{
		Resolution: resolution,
		Fallback:   fallback,
		Debug:      options.Debug,
	}
}

func fallbackEnabled(options *GeocodeOptions) bool {
	return options.Fallback == nil || *options.Fallback
}

func boolPtr(v bool) *bool {
	return &v
}
