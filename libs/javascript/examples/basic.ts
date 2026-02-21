import { ReverseGeocoder } from "../src/index.js";

const geocoder = ReverseGeocoder.getInstance();
const location = geocoder.geocode(28.6139, 77.209);

if (!location) {
  console.log("No location found");
} else {
  console.log(location);
}

