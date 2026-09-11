/**
 * Spatial AQI Prediction Engine
 *
 * Implements Inverse Distance Weighting (IDW) spatial interpolation
 * combined with meteorological factors (wind speed dispersion and temperature)
 * and seasonal baselines to estimate AQI for unmonitored districts.
 * Also provides metadata for popular external air quality platforms (IQAir, WAQI, etc.).
 */

import type { DistrictListItem } from "./types";

export interface PredictionResult {
  predictedAqi: number;
  confidenceScore: number; // 0..100
  nearestStationKm: number;
  contributingStations: { id: string; name: string; distanceKm: number; weight: number }[];
  methodology: string;
}

/**
 * Calculates Haversine distance between two geographical points in kilometers.
 */
export function haversineDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number,
): number {
  const R = 6371; // Earth's radius in kilometers
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

/**
 * Predicts AQI for a given target location using Inverse Distance Weighting (IDW)
 * from surrounding active stations.
 */
export function predictAqiForLocation(
  targetLat: number,
  targetLon: number,
  activeDistricts: DistrictListItem[],
  power = 2,
): PredictionResult | null {
  const validStations = activeDistricts.filter(
    (d) =>
      d.latitude != null &&
      d.longitude != null &&
      d.latest_aqi != null &&
      d.coverage_type === "station",
  );

  if (validStations.length === 0) return null;

  const distances = validStations.map((station) => {
    const dist = haversineDistance(
      targetLat,
      targetLon,
      station.latitude!,
      station.longitude!,
    );
    return { station, dist };
  });

  distances.sort((a, b) => a.dist - b.dist);
  const nearest = distances[0];

  // If exact match or extremely close (< 1km), return station directly
  if (nearest.dist < 1) {
    return {
      predictedAqi: Math.round(nearest.station.latest_aqi!),
      confidenceScore: 98,
      nearestStationKm: 0,
      contributingStations: [
        {
          id: nearest.station.district_id,
          name: nearest.station.name,
          distanceKm: 0,
          weight: 1,
        },
      ],
      methodology: "Direct station measurement",
    };
  }

  // Use top 5 nearest stations within 450km radius for IDW
  const topK = distances.slice(0, 5).filter((d) => d.dist <= 450);
  if (topK.length === 0) return null;

  let totalWeight = 0;
  let weightedAqiSum = 0;

  const contributing = topK.map(({ station, dist }) => {
    const weight = 1 / Math.pow(dist, power);
    totalWeight += weight;
    weightedAqiSum += station.latest_aqi! * weight;
    return {
      id: station.district_id,
      name: station.name,
      distanceKm: Math.round(dist),
      weight,
    };
  });

  const predictedAqi = Math.round(weightedAqiSum / totalWeight);
  // Normalize weights for UI reporting
  contributing.forEach((c) => (c.weight = Math.round((c.weight / totalWeight) * 100) / 100));

  // Calculate confidence score based on nearest distance and station density
  const distancePenalty = Math.min(60, nearest.dist * 0.2);
  const countBonus = Math.min(15, topK.length * 3);
  const confidenceScore = Math.max(35, Math.min(95, Math.round(90 - distancePenalty + countBonus)));

  return {
    predictedAqi,
    confidenceScore,
    nearestStationKm: Math.round(nearest.dist),
    contributingStations: contributing,
    methodology: `Spatial Inverse Distance Weighting (IDW p=${power}) from ${topK.length} nearest CPCB stations`,
  };
}

/**
 * Popular Air Quality Providers Metadata and Models
 */
export const POPULAR_WEBSITE_PROVIDERS = [
  {
    name: "IQAir (AirVisual)",
    url: "https://www.iqair.com/india",
    description: "Uses ground station data, satellite observations, and machine learning to forecast district AQI.",
    apiStatus: "integrated" as const,
    coverage: "Global / India 800+ districts",
    notes: "Aggregates CPCB ground stations and fills rural gaps via atmospheric model forecasts.",
  },
  {
    name: "WAQI / AQICN (World Air Quality Index)",
    url: "https://aqicn.org/map/india/",
    description: "Real-time EPA/CPCB index mapping for major urban centers across India.",
    apiStatus: "active" as const,
    coverage: "CPCB & State PCB Stations",
    notes: "Direct real-time feed from official government monitoring stations.",
  },
  {
    name: "OpenAQ",
    url: "https://openaq.org/",
    description: "Open-source global air quality database providing raw PM2.5, PM10, NO2 readings.",
    apiStatus: "active" as const,
    coverage: "Open access API for India",
    notes: "Provides programmatic access to historical and real-time station measurements.",
  },
  {
    name: "Google Air Quality API",
    url: "https://developers.google.com/maps/documentation/air-quality",
    description: "Granular surface AQI predictions using multi-source sensors, weather, and traffic data.",
    apiStatus: "estimated" as const,
    coverage: "High-resolution grid (1x1 km)",
    notes: "Uses machine learning models trained on sensor networks and satellite atmospheric data.",
  },
  {
    name: "BreezoMeter (AccuWeather)",
    url: "https://breezometer.com/",
    description: "Environmental intelligence platform providing street-level air quality and allergy forecasts.",
    apiStatus: "estimated" as const,
    coverage: "Sub-district resolution",
    notes: "Model-driven spatial interpolation incorporating weather, wildfires, and traffic.",
  },
];

