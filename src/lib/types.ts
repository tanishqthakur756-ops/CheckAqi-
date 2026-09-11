/** Type contracts matching the backend's Pydantic schemas. */

export type Season = "winter" | "summer" | "monsoon" | "post_monsoon";
export type CoverageType = "station" | "interpolated" | "predicted" | "no_data";

export interface DistrictListItem {
  district_id: string;
  name: string;
  state: string;
  latitude: number | null;
  longitude: number | null;
  latest_aqi: number | null;
  latest_date: string | null;
  coverage_type: CoverageType | null;
  prediction_confidence?: number;
  nearest_station_km?: number;
  is_predicted?: boolean;
}

export interface DistrictMeta {
  district_id: string;
  lgd_code: string | null;
  name: string;
  state: string;
  latitude: number | null;
  longitude: number | null;
}

export interface DistrictDetail {
  meta: DistrictMeta;
  active_station_count: number;
  prediction_info?: {
    confidence: number;
    nearest_station_km: number;
    interpolated_from: string[];
    methodology: string;
  };
}

export interface DistrictRollup {
  district_id: string;
  date: string;
  avg_aqi: number | null;
  max_aqi: number | null;
  avg_temp: number | null;
  avg_rainfall: number | null;
  avg_wind: number | null;
  season: Season;
  station_count: number;
  coverage_type: CoverageType;
}

export interface HistoryResponse {
  district_id: string;
  range: "30d" | "90d" | "1y";
  data: DistrictRollup[];
}

export interface SeasonalPattern {
  winter: number | null;
  summer: number | null;
  monsoon: number | null;
  post_monsoon: number | null;
}

export interface CorrelationResponse {
  seasonal_pattern: SeasonalPattern | null;
  wind_correlation: number | null;
  rainfall_correlation: number | null;
}

export interface SourceInfo {
  source_name: string;
  source_url: string | null;
  license_note: string | null;
  last_synced_at: string | null;
  category?: "official" | "weather" | "popular_website" | "model";
  coverage_description?: string;
  api_status?: "active" | "integrated" | "estimated";
}
