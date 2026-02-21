package config

import (
	"fmt"
	"path/filepath"
	"runtime"
)

const (
	MinResolution     = 4
	MaxResolution     = 5
	DefaultResolution = MaxResolution
	DataDirName       = "data"
	DataFilePrefix    = "reverse_geo_"
)

var SupportedResolutions = []int{4, 5}

func ClampResolution(resolution int) int {
	if resolution < MinResolution {
		return MinResolution
	}
	if resolution > MaxResolution {
		return MaxResolution
	}
	return resolution
}

func dataDirPath() string {
	_, currentFile, _, ok := runtime.Caller(0)
	if !ok {
		return filepath.Join(DataDirName)
	}
	// internal/config -> module root
	return filepath.Join(filepath.Dir(currentFile), "..", "..", DataDirName)
}

func DataFilePath(resolution int) string {
	return filepath.Join(dataDirPath(), fmt.Sprintf("%s%d.json", DataFilePrefix, resolution))
}
