/**
 * Loaders that try the live API first and fall back to the bundled
 * sample dataset if the request fails. This lets the static dashboard
 * work both with and without the FastAPI backend reachable.
 */

import { api } from "./api";
import {
  SAMPLE_DISTRICTS,
  SAMPLE_SOURCES,
  getSampleCorrelation,
  getSampleDistrict,
  getSampleHistory,
} from "./sampleData";
import type {
  CorrelationResponse,
  DistrictDetail,
  DistrictListItem,
  HistoryResponse,
  SourceInfo,
} from "./types";

export interface LoadResult<T> {
  data: T;
  /** Did this come from the live API or the bundled sample? */
  source: "live" | "sample";
}

async function withFallback<T>(
  loader: () => Promise<T>,
  fallback: () => T | null,
): Promise<LoadResult<T> | null> {
  try {
    const data = await loader();
    return { data, source: "live" };
  } catch (err) {
    const fallbackData = fallback();
    if (fallbackData == null) return null;
    return { data: fallbackData, source: "sample" };
  }
}

export async function loadDistricts(): Promise<LoadResult<DistrictListItem[]>> {
  const res = await withFallback<DistrictListItem[]>(
    () => api.listDistricts(),
    () => SAMPLE_DISTRICTS,
  );
  return res ?? { data: SAMPLE_DISTRICTS, source: "sample" };
}

export async function loadDistrict(
  id: string,
): Promise<LoadResult<DistrictDetail> | null> {
  return withFallback<DistrictDetail>(
    () => api.district(id),
    () => getSampleDistrict(id),
  );
}

export async function loadHistory(
  id: string,
  range: "30d" | "90d" | "1y" = "1y",
): Promise<LoadResult<HistoryResponse> | null> {
  return withFallback<HistoryResponse>(
    () => api.history(id, range),
    () => getSampleHistory(id, range),
  );
}

export async function loadCorrelation(
  id: string,
): Promise<LoadResult<CorrelationResponse> | null> {
  return withFallback<CorrelationResponse>(
    () => api.correlation(id),
    () => getSampleCorrelation(id),
  );
}

export async function loadSources(): Promise<LoadResult<SourceInfo[]>> {
  const res = await withFallback<SourceInfo[]>(
    () => api.sources(),
    () => SAMPLE_SOURCES,
  );
  return res ?? { data: SAMPLE_SOURCES, source: "sample" };
}
