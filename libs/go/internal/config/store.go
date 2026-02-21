package config

import (
	"encoding/json"
	"os"
)

type LocationDetails struct {
	City     string  `json:"city"`
	State    string  `json:"state"`
	District *string `json:"district,omitempty"`
	Pincode  *string `json:"pincode,omitempty"`
}

type ReverseGeoStore map[string]LocationDetails

func ReadReverseGeoStore(resolution int) ReverseGeoStore {
	filePath := DataFilePath(resolution)
	if _, err := os.Stat(filePath); err != nil {
		return ReverseGeoStore{}
	}

	raw, err := os.ReadFile(filePath)
	if err != nil {
		return ReverseGeoStore{}
	}

	store := ReverseGeoStore{}
	if err := json.Unmarshal(raw, &store); err != nil {
		return ReverseGeoStore{}
	}
	return store
}
