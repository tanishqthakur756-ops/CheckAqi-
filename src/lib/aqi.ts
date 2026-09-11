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
