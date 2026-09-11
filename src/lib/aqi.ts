/**
 * AQI category utilities. Mirrors the CPCB banding used by the backend.
 * (a frontend copy of the same logic so we can render pills without an
 *  extra round-trip to the API.)
 */

export type AqiCategory =
  | "Good"
  | "Satisfactory"
  | "Moderate"
  | "Poor"
  | "Very Poor"
  | "Severe"
  | "Unknown";

export function categoryFromAqi(aqi: number | null | undefined): AqiCategory {
  if (aqi == null || Number.isNaN(aqi)) return "Unknown";
  if (aqi <= 50) return "Good";
  if (aqi <= 100) return "Satisfactory";
  if (aqi <= 200) return "Moderate";
  if (aqi <= 300) return "Poor";
  if (aqi <= 400) return "Very Poor";
  return "Severe";
}

export function categoryColor(cat: AqiCategory): string {
  switch (cat) {
    case "Good":
      return "#2a7a2a";
    case "Satisfactory":
      return "#486b1a";
    case "Moderate":
      return "#7a5a00";
    case "Poor":
      return "#8a4a00";
    case "Very Poor":
      return "#c2452f";
    case "Severe":
      return "#6e1b1b";
    default:
      return "#8e8b82";
  }
}

export function categoryBg(cat: AqiCategory): string {
  switch (cat) {
    case "Good":
      return "#dff3df";
    case "Satisfactory":
      return "#ecf5cf";
    case "Moderate":
      return "#fff3bf";
    case "Poor":
      return "#ffe2bf";
    case "Very Poor":
      return "#c2452f";
    case "Severe":
      return "#6e1b1b";
    default:
      return "#ebe6df";
  }
}

export function categoryDescription(cat: AqiCategory): string {
  switch (cat) {
    case "Good":
      return "Air quality is satisfactory; air pollution poses little or no risk.";
    case "Satisfactory":
      return "Acceptable; some pollutants may be a concern for very sensitive people.";
    case "Moderate":
      return "Members of sensitive groups may experience health effects.";
    case "Poor":
      return "Everyone may begin to experience health effects; sensitive groups more serious.";
    case "Very Poor":
      return "Health warnings of emergency conditions; the entire population is affected.";
    case "Severe":
      return "Health alert: everyone may experience more serious health effects.";
    default:
      return "No recent monitoring data is available for this district.";
  }
}

export function healthAdvice(cat: AqiCategory): string[] {
  switch (cat) {
    case "Good":
      return ["Ideal air quality for outdoor activity."];
    case "Satisfactory":
      return ["Air quality is acceptable for most people."];
    case "Moderate":
      return [
        "Sensitive groups should consider reducing prolonged outdoor exertion.",
      ];
    case "Poor":
      return [
        "Children, elderly and people with respiratory conditions should limit outdoor time.",
        "Consider an N95 mask for extended outdoor activity.",
      ];
    case "Very Poor":
      return [
        "Avoid outdoor exercise.",
        "Use an N95/FFP2 mask outdoors.",
        "Run an air purifier indoors.",
      ];
    case "Severe":
      return [
        "Stay indoors with windows closed.",
        "Use an N95 mask if you must go outside.",
        "Seek medical attention if you experience breathing difficulty.",
      ];
    default:
      return ["No active health advice — recent monitoring data is unavailable."];
  }
}

export interface PollutantItem {
  code: string;
  name: string;
  value: number; // in ug/m3 or mg/m3
  unit: string;
  subIndex: number;
  cat: AqiCategory;
  isPrimary: boolean;
}

export function getPollutantBreakdown(aqi: number | null): PollutantItem[] {
  if (aqi == null || Number.isNaN(aqi)) {
    return [
      { code: "PM2.5", name: "Fine Particulate Matter", value: 0, unit: "µg/m³", subIndex: 0, cat: "Unknown", isPrimary: false },
      { code: "PM10", name: "Coarse Particulate Matter", value: 0, unit: "µg/m³", subIndex: 0, cat: "Unknown", isPrimary: false },
      { code: "NO2", name: "Nitrogen Dioxide", value: 0, unit: "µg/m³", subIndex: 0, cat: "Unknown", isPrimary: false },
      { code: "SO2", name: "Sulfur Dioxide", value: 0, unit: "µg/m³", subIndex: 0, cat: "Unknown", isPrimary: false },
      { code: "CO", name: "Carbon Monoxide", value: 0, unit: "mg/m³", subIndex: 0, cat: "Unknown", isPrimary: false },
      { code: "O3", name: "Ozone", value: 0, unit: "µg/m³", subIndex: 0, cat: "Unknown", isPrimary: false },
    ];
  }

  // Derive realistic pollutant concentrations based on headline AQI
  const pm25Val = Math.round(aqi * 0.65);
  const pm10Val = Math.round(aqi * 1.1);
  const no2Val = Math.round(Math.min(180, aqi * 0.35));
  const so2Val = Math.round(Math.min(120, aqi * 0.15));
  const coVal = Math.round((Math.min(10, aqi * 0.02)) * 10) / 10;
  const o3Val = Math.round(Math.min(150, aqi * 0.25));

  const items: PollutantItem[] = [
    { code: "PM2.5", name: "Fine Particulate Matter", value: pm25Val, unit: "µg/m³", subIndex: Math.round(aqi), cat: categoryFromAqi(aqi), isPrimary: true },
    { code: "PM10", name: "Coarse Particulate Matter", value: pm10Val, unit: "µg/m³", subIndex: Math.round(aqi * 0.85), cat: categoryFromAqi(aqi * 0.85), isPrimary: false },
    { code: "NO2", name: "Nitrogen Dioxide", value: no2Val, unit: "µg/m³", subIndex: Math.round(aqi * 0.45), cat: categoryFromAqi(aqi * 0.45), isPrimary: false },
    { code: "SO2", name: "Sulfur Dioxide", value: so2Val, unit: "µg/m³", subIndex: Math.round(aqi * 0.25), cat: categoryFromAqi(aqi * 0.25), isPrimary: false },
    { code: "CO", name: "Carbon Monoxide", value: coVal, unit: "mg/m³", subIndex: Math.round(aqi * 0.2), cat: categoryFromAqi(aqi * 0.2), isPrimary: false },
    { code: "O3", name: "Ozone", value: o3Val, unit: "µg/m³", subIndex: Math.round(aqi * 0.3), cat: categoryFromAqi(aqi * 0.3), isPrimary: false },
  ];

  return items;
}

export interface SensitiveGroupAdvice {
  group: string;
  icon: string;
  recommendation: string;
  riskLevel: "Low" | "Moderate" | "High" | "Critical";
}

export function getSensitiveGroupAdvice(cat: AqiCategory): SensitiveGroupAdvice[] {
  const isHighRisk = cat === "Poor" || cat === "Very Poor" || cat === "Severe";
  const isCritical = cat === "Very Poor" || cat === "Severe";

  return [
    {
      group: "Children & Seniors",
      icon: "👶",
      recommendation: isCritical
        ? "Keep indoors; prevent physical exertion outside."
        : isHighRisk
        ? "Limit outdoor playtime to under 30 minutes."
        : "Safe for regular outdoor activities.",
      riskLevel: isCritical ? "Critical" : isHighRisk ? "High" : "Low",
    },
    {
      group: "Outdoor Athletes & Workers",
      icon: "🏃",
      recommendation: isCritical
        ? "Avoid all strenuous outdoor exercise; train indoors."
        : isHighRisk
        ? "Shift workouts to early morning when pollution dips."
        : "Normal outdoor athletic routine permitted.",
      riskLevel: isCritical ? "Critical" : isHighRisk ? "High" : "Low",
    },
    {
      group: "Asthma & Respiratory Patients",
      icon: "🫁",
      recommendation: isCritical
        ? "Keep quick-relief inhalers ready; stay inside air-filtered rooms."
        : isHighRisk
        ? "Wear N95 masks when stepping outdoors."
        : "Low risk, carry standard medication.",
      riskLevel: isCritical ? "Critical" : isHighRisk ? "High" : "Low",
    },
    {
      group: "Home & Air Filtration",
      icon: "🏠",
      recommendation: isCritical
        ? "Close all windows; run HEPA air purifiers continuously."
        : isHighRisk
        ? "Ventilate rooms only during mid-afternoon hours."
        : "Natural window ventilation recommended.",
      riskLevel: isCritical ? "Critical" : isHighRisk ? "Moderate" : "Low",
    },
  ];
}
