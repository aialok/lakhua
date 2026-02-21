package main

import (
	"fmt"

	lakhua "github.com/aialok/lakhua/libs/go"
)

func main() {
	result := lakhua.Geocode(28.6139, 77.2090, &lakhua.GeocodeOptions{Debug: true})
	if result == nil {
		fmt.Println("no match")
		return
	}
	fmt.Printf("city=%s state=%s matched_h3=%s matched_resolution=%d\n", result.City, result.State, result.MatchedH3, result.MatchedResolution)
}
