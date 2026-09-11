/**
 * API client for the India AQI backend.
 *
 * The frontend is a static site — the backend lives at a different origin in
 * production. `PUBLIC_API_BASE` lets the deployer point at a real FastAPI
 * instance, while the default empty string keeps the dashboard working in
 * the demo (same-origin via the FastAPI static mount).
 */

import type {
  CorrelationResponse,
  DistrictDetail,
  DistrictListItem,
  HistoryResponse,
  SourceInfo,
} from "./types";

const DEFAULT_BASE = "http://127.0.0.1:8000";

function getBase(): string {
  // Astro exposes import.meta.env at build time; we keep the prefix
  // PUBLIC_ so the value is inlined into the client bundle.
  const fromEnv =
    typeof import.meta !== "undefined" &&
    (import.meta as any).env &&
    (import.meta as any).env.PUBLIC_API_BASE;
  if (fromEnv && typeof fromEnv === "string" && fromEnv.length > 0) {
    return fromEnv.replace(/\/$/, "");
  }
  return DEFAULT_BASE;
}

async function getJson<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${getBase()}${path}`;
  const res = await fetch(url, {
    ...init,
    headers: { Accept: "application/json", ...(init?.headers ?? {}) },
  });
  if (!res.ok) {
    throw new Error(`API ${path} -> ${res.status}`);
  }
  return (await res.json()) as T;
}

export const api = {
  base: getBase,
  listDistricts: () => getJson<DistrictListItem[]>("/api/districts/"),
  district: (id: string) => getJson<DistrictDetail>(`/api/districts/${id}`),
  history: (id: string, range: "30d" | "90d" | "1y" = "1y") =>
    getJson<HistoryResponse>(`/api/districts/${id}/history?range=${range}`),
  correlation: (id: string) =>
    getJson<CorrelationResponse>(`/api/districts/${id}/correlation`),
  sources: () => getJson<SourceInfo[]>("/api/sources/"),
};
