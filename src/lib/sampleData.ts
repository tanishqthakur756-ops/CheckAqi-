/**
 * Static fallback dataset for the India AQI tracker.
 *
 * The frontend is a static site and may be deployed without the FastAPI
 * backend. To keep the dashboard fully usable in that case, we ship a
 * deterministic, seed-style sample dataset that mirrors the shape of the
 * backend responses exactly. When the API is reachable, the live data
 * supersedes it; otherwise the same code path renders the demo numbers
 * so the site is still demonstrable end-to-end.
 *
 * Numbers here are illustrative, not real measurements.
 */

import type {
  CorrelationResponse,
  DistrictDetail,
  DistrictListItem,
  DistrictRollup,
  HistoryResponse,
  SeasonalPattern,
  SourceInfo,
} from "./types";

// --- helpers used to synthesize consistent per-district data -----------
function hash(str: string): number {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = (h * 16777619) >>> 0;
  }
  return h;
}
function rand(seed: number): () => number {
  let s = seed || 1;
  return () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 0xffffffff;
  };
}

interface Seed {
  id: string;
  name: string;
  state: string;
  lat: number;
  lon: number;
  /** rough baseline AQI, used to give the dashboard meaningful variation */
  baseAqi: number;
}

const SEEDS: Seed[] = [
  { id: "dl_delhi", name: "Central Delhi", state: "Delhi", lat: 28.6139, lon: 77.209, baseAqi: 280 },
  { id: "dl_east", name: "East Delhi", state: "Delhi", lat: 28.5749, lon: 77.282, baseAqi: 295 },
  { id: "dl_new", name: "New Delhi", state: "Delhi", lat: 28.5355, lon: 77.391, baseAqi: 260 },
  { id: "dl_north", name: "North Delhi", state: "Delhi", lat: 28.6792, lon: 77.164, baseAqi: 270 },
  { id: "dl_north_east", name: "Northeast Delhi", state: "Delhi", lat: 28.6369, lon: 77.293, baseAqi: 310 },
  { id: "dl_north_west", name: "Northwest Delhi", state: "Delhi", lat: 28.721, lon: 77.12, baseAqi: 290 },
  { id: "dl_south", name: "South Delhi", state: "Delhi", lat: 28.45, lon: 77.15, baseAqi: 230 },
  { id: "dl_south_east", name: "Southeast Delhi", state: "Delhi", lat: 28.52, lon: 77.22, baseAqi: 245 },
  { id: "dl_south_west", name: "Southwest Delhi", state: "Delhi", lat: 28.4, lon: 77.1, baseAqi: 220 },
  { id: "dl_west", name: "West Delhi", state: "Delhi", lat: 28.62, lon: 77.1, baseAqi: 265 },
  { id: "mh_mumbai", name: "Mumbai", state: "Maharashtra", lat: 19.076, lon: 72.8777, baseAqi: 145 },
  { id: "mh_pune", name: "Pune", state: "Maharashtra", lat: 18.5204, lon: 73.8567, baseAqi: 130 },
  { id: "mh_nagpur", name: "Nagpur", state: "Maharashtra", lat: 21.1458, lon: 79.0882, baseAqi: 155 },
  { id: "mh_nashik", name: "Nashik", state: "Maharashtra", lat: 19.9935, lon: 73.793, baseAqi: 120 },
  { id: "mh_akola", name: "Akola", state: "Maharashtra", lat: 20.7, lon: 79.0, baseAqi: 140 },
  { id: "tn_chennai", name: "Chennai", state: "Tamil Nadu", lat: 13.0827, lon: 80.2747, baseAqi: 105 },
  { id: "tn_coimbatore", name: "Coimbatore", state: "Tamil Nadu", lat: 11.0168, lon: 77.005, baseAqi: 88 },
  { id: "tn_madurai", name: "Madurai", state: "Tamil Nadu", lat: 9.9252, lon: 78.1549, baseAqi: 95 },
  { id: "tn_virudhunagar", name: "Virudhunagar", state: "Tamil Nadu", lat: 9.801, lon: 77.9, baseAqi: 90 },
  { id: "ka_bengaluru", name: "Bengaluru", state: "Karnataka", lat: 12.9716, lon: 77.5946, baseAqi: 110 },
  { id: "ka_mysuru", name: "Mysuru", state: "Karnataka", lat: 12.2958, lon: 76.6394, baseAqi: 75 },
  { id: "ka_hubli", name: "Hubli", state: "Karnataka", lat: 15.3647, lon: 75.128, baseAqi: 95 },
  { id: "wb_kolkata", name: "Kolkata", state: "West Bengal", lat: 22.5726, lon: 88.3639, baseAqi: 180 },
  { id: "wb_siliguri", name: "North Dinajpur", state: "West Bengal", lat: 26.3, lon: 88.6, baseAqi: 130 },
  { id: "wb_howrah", name: "Howrah", state: "West Bengal", lat: 22.5958, lon: 88.2636, baseAqi: 175 },
  { id: "gj_ahmedabad", name: "Ahmedabad", state: "Gujarat", lat: 23.2156, lon: 72.5563, baseAqi: 165 },
  { id: "gj_surat", name: "Surat", state: "Gujarat", lat: 21.1702, lon: 72.5714, baseAqi: 140 },
  { id: "gj_vadodara", name: "Vadodara", state: "Gujarat", lat: 22.3072, lon: 73.1812, baseAqi: 135 },
  { id: "rj_jaipur", name: "Jaipur", state: "Rajasthan", lat: 26.9124, lon: 75.7873, baseAqi: 175 },
  { id: "rj_jodhpur", name: "Jodhpur", state: "Rajasthan", lat: 26.2124, lon: 73.007, baseAqi: 165 },
  { id: "rj_kota", name: "Kota", state: "Rajasthan", lat: 25.2138, lon: 75.5828, baseAqi: 155 },
  { id: "pb_ludhiana", name: "Ludhiana", state: "Punjab", lat: 30.9, lon: 75.85, baseAqi: 195 },
  { id: "pb_amohta", name: "Amritsar", state: "Punjab", lat: 31.638, lon: 74.872, baseAqi: 175 },
  { id: "hr_chandigarh", name: "Chandigarh", state: "Haryana", lat: 30.7333, lon: 76.7833, baseAqi: 170 },
  { id: "hr_faridabad", name: "Faridabad", state: "Haryana", lat: 28.4089, lon: 77.3178, baseAqi: 245 },
  { id: "hr_gurgaon", name: "Gurugram", state: "Haryana", lat: 28.4595, lon: 77.0266, baseAqi: 240 },
  { id: "uk_dehradun", name: "Dehradun", state: "Uttarakhand", lat: 30.3165, lon: 78.0322, baseAqi: 110 },
  { id: "uk_nainital", name: "Nainital", state: "Uttarakhand", lat: 29.3919, lon: 79.6238, baseAqi: 65 },
  { id: "hp_shimla", name: "Shimla", state: "Himachal Pradesh", lat: 31.1042, lon: 77.1722, baseAqi: 55 },
  { id: "jk_srinagar", name: "Srinagar", state: "Jammu and Kashmir", lat: 34.0837, lon: 74.7973, baseAqi: 60 },
  { id: "jk_jammu", name: "Jammu", state: "Jammu and Kashmir", lat: 32.7192, lon: 74.9636, baseAqi: 120 },
  { id: "as_guwaahati", name: "Kamrup", state: "Assam", lat: 26.1406, lon: 91.772, baseAqi: 90 },
  { id: "as_dispur", name: "Kokrajhar", state: "Assam", lat: 26.4, lon: 90.25, baseAqi: 75 },
  { id: "br_patna", name: "Patna", state: "Bihar", lat: 25.6125, lon: 85.1416, baseAqi: 200 },
  { id: "br_gaya", name: "Gaya", state: "Bihar", lat: 24.795, lon: 85.3125, baseAqi: 180 },
  { id: "od_bhubaneswar", name: "Khordha", state: "Odisha", lat: 20.2961, lon: 85.8189, baseAqi: 110 },
  { id: "od_cuttack", name: "Cuttack", state: "Odisha", lat: 20.4625, lon: 85.857, baseAqi: 115 },
  { id: "tg_hyderabad", name: "Hyderabad", state: "Telangana", lat: 17.361, lon: 78.478, baseAqi: 125 },
  { id: "tg_warangal", name: "Warangal", state: "Telangana", lat: 17.9748, lon: 79.531, baseAqi: 105 },
  { id: "ap_vijayawada", name: "Krishna", state: "Andhra Pradesh", lat: 16.422, lon: 80.424, baseAqi: 115 },
  { id: "ap_visakhapatnam", name: "Visakhapatnam", state: "Andhra Pradesh", lat: 17.68, lon: 83.21, baseAqi: 100 },
  { id: "ap_guntur", name: "Guntur", state: "Andhra Pradesh", lat: 16.21, lon: 80.95, baseAqi: 110 },
  { id: "kl_thiruvananthapuram", name: "Thiruvananthapuram", state: "Kerala", lat: 8.5241, lon: 76.9366, baseAqi: 70 },
  { id: "kl_kochi", name: "Ernakulam", state: "Kerala", lat: 10.077, lon: 76.274, baseAqi: 80 },
  { id: "kl_kozhikode", name: "Kozhikode", state: "Kerala", lat: 11.2588, lon: 75.782, baseAqi: 75 },
  { id: "mp_bhopal", name: "Bhopal", state: "Madhya Pradesh", lat: 23.2599, lon: 77.4128, baseAqi: 150 },
  { id: "mp_indore", name: "Indore", state: "Madhya Pradesh", lat: 22.7196, lon: 75.9273, baseAqi: 140 },
  { id: "mp_jabalpur", name: "Jabalpur", state: "Madhya Pradesh", lat: 23.1613, lon: 79.9567, baseAqi: 130 },
  { id: "cg_raipur", name: "Raipur", state: "Chhattisgarh", lat: 18.615, lon: 81.86, baseAqi: 145 },
  { id: "cg_bilaspur", name: "Bilaspur", state: "Chhattisgarh", lat: 18.107, lon: 81.31, baseAqi: 135 },
  { id: "jh_ranchi", name: "Ranchi", state: "Jharkhand", lat: 23.3403, lon: 85.3076, baseAqi: 130 },
  { id: "jh_jamshedpur", name: "Saraikela", state: "Jharkhand", lat: 22.774, lon: 85.65, baseAqi: 140 },
  { id: "up_lucknow", name: "Lucknow", state: "Uttar Pradesh", lat: 26.8499, lon: 80.9498, baseAqi: 195 },
  { id: "up_kanpur", name: "Kanpur Nagar", state: "Uttar Pradesh", lat: 26.4292, lon: 80.3342, baseAqi: 220 },
  { id: "up_agra", name: "Agra", state: "Uttar Pradesh", lat: 27.1751, lon: 78.0421, baseAqi: 210 },
  { id: "up_varanasi", name: "Varanasi", state: "Uttar Pradesh", lat: 25.3176, lon: 82.9739, baseAqi: 200 },
  { id: "up_noida", name: "Gautam Buddha Nagar", state: "Uttar Pradesh", lat: 28.5355, lon: 77.391, baseAqi: 250 },
  { id: "up_ghaziabad", name: "Ghaziabad", state: "Uttar Pradesh", lat: 28.6692, lon: 77.41, baseAqi: 260 },
  { id: "up_bareilly", name: "Bareilly", state: "Uttar Pradesh", lat: 28.367, lon: 79.43, baseAqi: 185 },
];

function seasonFor(month: number): "winter" | "summer" | "monsoon" | "post_monsoon" {
  if (month === 12 || month <= 2) return "winter";
  if (month <= 5) return "summer";
  if (month <= 9) return "monsoon";
  return "post_monsoon";
}

function seasonalMultiplier(season: "winter" | "summer" | "monsoon" | "post_monsoon"): number {
  switch (season) {
    case "winter":
      return 1.35;
    case "summer":
      return 1.1;
    case "monsoon":
      return 0.7;
    case "post_monsoon":
      return 1.15;
  }
}

function tempFor(season: "winter" | "summer" | "monsoon" | "post_monsoon", r: number): number {
  const base: Record<typeof season, number> = {
    winter: 14,
    summer: 33,
    monsoon: 28,
    post_monsoon: 22,
  };
  return Math.round((base[season] + (r() - 0.5) * 4) * 10) / 10;
}
function rainfallFor(season: "winter" | "summer" | "monsoon" | "post_monsoon", r: number): number {
  const base: Record<typeof season, number> = {
    winter: 0.4,
    summer: 1.0,
    monsoon: 6.5,
    post_monsoon: 1.4,
  };
  return Math.round(base[season] * r() * 10) / 10;
}
function windFor(r: number): number {
  return Math.round((8 + r() * 12) * 10) / 10;
}

// --- public sample dataset -------------------------------------------

export const SAMPLE_DISTRICTS: DistrictListItem[] = SEEDS.map((s) => {
  const seedRng = rand(hash(s.id));
  const jitter = (seedRng() - 0.5) * 60;
  const latestAqi = Math.max(15, Math.round(s.baseAqi + jitter));
  // Build a recent "as-of" date deterministically
  const today = new Date("2026-08-31T00:00:00Z");
  const date = new Date(today.getTime() - Math.floor(seedRng() * 5) * 86400000);
  return {
    district_id: s.id,
    name: s.name,
    state: s.state,
    latitude: s.lat,
    longitude: s.lon,
    latest_aqi: latestAqi,
    latest_date: date.toISOString().slice(0, 10),
    coverage_type: "station" as const,
  };
});

const SAMPLE_LOOKUP = new Map(SEEDS.map((s) => [s.id, s]));

export function getSampleDistrict(id: string): DistrictDetail | null {
  const s = SAMPLE_LOOKUP.get(id);
  if (!s) return null;
  return {
    meta: {
      district_id: s.id,
      lgd_code: s.id.slice(0, 6).toUpperCase(),
      name: s.name,
      state: s.state,
      latitude: s.lat,
      longitude: s.lon,
    },
    active_station_count: 1 + (hash(s.id) % 3),
  };
}

export function getSampleHistory(
  id: string,
  range: "30d" | "90d" | "1y" = "1y",
): HistoryResponse | null {
  const s = SAMPLE_LOOKUP.get(id);
  if (!s) return null;
  const days = range === "30d" ? 30 : range === "90d" ? 90 : 365;
  const r = rand(hash(s.id + range));
  const today = new Date("2026-08-31T00:00:00Z");
  const data: DistrictRollup[] = [];
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(today.getTime() - i * 86400000);
    const month = d.getUTCMonth() + 1;
    const season = seasonFor(month);
    const baseAqi = s.baseAqi * seasonalMultiplier(season);
    const aqi = Math.max(
      20,
      Math.round(baseAqi + (r() - 0.5) * 60),
    );
    const temp = tempFor(season, r);
    const rain = rainfallFor(season, r);
    const wind = windFor(r);
    data.push({
      district_id: s.id,
      date: d.toISOString().slice(0, 10),
      avg_aqi: aqi,
      max_aqi: Math.round(aqi + 30 + r() * 20),
      avg_temp: temp,
      avg_rainfall: rain,
      avg_wind: wind,
      season,
      station_count: 1,
      coverage_type: i < 7 ? "interpolated" : "station",
    });
  }
  return { district_id: s.id, range, data };
}

export function getSampleCorrelation(id: string): CorrelationResponse | null {
  const s = SAMPLE_LOOKUP.get(id);
  if (!s) return null;
  const r = rand(hash(s.id + "corr"));
  const seasonal: SeasonalPattern = {
    winter: Math.round(s.baseAqi * 1.35 + (r() - 0.5) * 25),
    summer: Math.round(s.baseAqi * 1.1 + (r() - 0.5) * 20),
    monsoon: Math.round(s.baseAqi * 0.7 + (r() - 0.5) * 15),
    post_monsoon: Math.round(s.baseAqi * 1.15 + (r() - 0.5) * 20),
  };
  return {
    seasonal_pattern: seasonal,
    wind_correlation: Math.round((r() - 0.3) * 100) / 100,
    rainfall_correlation: Math.round((r() - 0.4) * 100) / 100,
  };
}

export const SAMPLE_SOURCES: SourceInfo[] = [
  {
    source_name: "CPCB",
    source_url: "https://data.gov.in/resources/cpcb-air-quality-data",
    license_note: "Open Government License (India)",
    last_synced_at: "2026-08-31T15:00:00+05:30",
  },
  {
    source_name: "Open-Meteo",
    source_url: "https://open-meteo.com/",
    license_note: "CC BY 4.0",
    last_synced_at: "2026-08-31T14:00:00+00:00",
  },
  {
    source_name: "IMD",
    source_url: "https://data.gov.in/resources/imd-historical-data",
    license_note: "Open Government License (India)",
    last_synced_at: "2026-08-31T12:00:00+05:30",
  },
];
