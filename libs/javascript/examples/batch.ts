import { ReverseGeocoder } from "../src/index.js";

const points: Array<[number, number]> = [
  [28.6139, 77.209],
  [19.076, 72.8777],
  [12.9716, 77.5946],
];

const geocoder = ReverseGeocoder.getInstance();
const results = points.map(([lat, lon]) => geocoder.geocode(lat, lon));
console.log(results);
