"""
Real CPCB ingestion. This pulls live data from data.gov.in and turns it into
the same shape our website's database expects (one row per station per day,
not one row per pollutant per station).

Run this from inside the backend/ folder:
    python ingest_cpcb_live.py

This is still a DRY RUN -- it fetches and prints, but does NOT save to your
database yet. Once you see this working correctly, we'll add the "save it"
step.
"""
import os
import re
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

from dotenv import load_dotenv

from app.analytics.aqi_calculator import compute_station_aqi

load_dotenv()

API_KEY = os.getenv("CPCB_API_KEY")
RESOURCE_ID = "3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"
BASE_URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"

# CPCB gives city/state, not a district_id -- this maps the cities we know
# about (matching your seeded districts) to your district_id slugs. Any city
# NOT in this list gets skipped for now rather than guessed at.
# TODO: expand this as you add more districts to seed_districts.sql.
CITY_TO_DISTRICT = {
    ("Delhi", "Delhi"): "dl_delhi",
    ("Mumbai", "Maharashtra"): "mh_mumbai",
    ("Bengaluru", "Karnataka"): "ka_bengaluru_urban",
    # add more (city, state) -> district_id pairs here as needed
}


def slugify(text: str) -> str:
    """Turn a station name into a safe, stable ID (since CPCB gives no numeric ID)."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def safe_float(value):
    """CPCB uses the literal string "NA" for missing readings -- catch that."""
    if value is None:
        return None
    if isinstance(value, str) and value.strip().upper() in ("NA", ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fetch_page(offset: int, limit: int = 10, max_retries: int = 4, timeout_seconds: int = 30):
    params = {"api-key": API_KEY, "format": "json", "limit": limit, "offset": offset}
    url = f"{BASE_URL}?" + urllib.parse.urlencode(params)

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout_seconds) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            print(f"  Server error at offset {offset}: HTTP {e.code}")
            raise
        except (TimeoutError, urllib.error.URLError) as e:
            last_error = e
            print(f"  Timeout at offset {offset}, attempt {attempt}/{max_retries}...")
            if attempt < max_retries:
                time.sleep(3)
    raise last_error


def fetch_all_records(max_pages: int = 20, page_size: int = 10):
    """
    Pages through the API. NOTE: the public sample key caps each request at
    10 records -- pulling all ~3500 India-wide readings this way means ~350
    requests, which the sample key isn't meant for (you'll likely get rate-
    limited or blocked). max_pages defaults to a small number so this stays
    a safe test. Once you have a REAL personal key with a higher limit
    parameter (e.g. limit=1000), this same function works, just faster.
    """
    all_records = []
    offset = 0
    for page in range(max_pages):
        print(f"Fetching page {page + 1} (offset {offset})...")
        result = fetch_page(offset=offset, limit=page_size)
        records = result.get("records", [])
        if not records:
            break
        all_records.extend(records)
        offset += page_size
        total = result.get("total")
        if total and offset >= int(total):
            break
        time.sleep(1)  # be polite to a free government API
    return all_records


def pivot_records_to_stations(records: list[dict]) -> dict:
    """
    THE FIX FROM EARLIER: CPCB gives one row per pollutant per station.
    Group them into one composite reading per station, the shape our
    database (and aqi_calculator) actually expects.
    """
    stations = {}

    for row in records:
        station_name = row.get("station", "").strip()
        city = row.get("city", "").strip()
        state = row.get("state", "").strip()
        if not station_name:
            continue

        station_id = slugify(station_name)
        district_id = CITY_TO_DISTRICT.get((city, state))

        if station_id not in stations:
            stations[station_id] = {
                "station_id": station_id,
                "station_name": station_name,
                "city": city,
                "state": state,
                "district_id": district_id,  # may be None -- see below
                "latitude": safe_float(row.get("latitude")),
                "longitude": safe_float(row.get("longitude")),
                "last_update": row.get("last_update"),
                "pollutants": {},
            }

        pollutant_id = (row.get("pollutant_id") or "").strip().upper()
        avg_value = safe_float(row.get("avg_value"))
        if avg_value is None:
            continue  # this pollutant's reading is "NA" right now, skip it

        # Map CPCB's pollutant names to our calculator's expected keys
        key_map = {
            "PM2.5": "pm2_5", "PM10": "pm10", "NO2": "no2", "SO2": "so2",
            "CO": "co", "NH3": "nh3", "OZONE": "o3", "O3": "o3",
        }
        key = key_map.get(pollutant_id)
        if key:
            stations[station_id]["pollutants"][key] = avg_value

    return stations


def compute_aqi_for_all_stations(stations: dict):
    for station_id, data in stations.items():
        pollutants = {k: v for k, v in data["pollutants"].items() if k != "o3"}
        # NOTE: CPCB's real-time feed doesn't say whether O3 is an 8-hr or
        # 1-hr average -- we're assuming 8-hr here since that's what their
        # live dashboard typically reports. Worth double-checking against
        # CPCB's own documentation if O3 numbers ever look suspicious.
        o3_readings = None
        if "o3" in data["pollutants"]:
            o3_readings = {"8h": data["pollutants"]["o3"]}

        result = compute_station_aqi(pollutants, o3_readings=o3_readings)
        data["aqi_result"] = result


if __name__ == "__main__":
    if not API_KEY:
        print("No CPCB_API_KEY found in your .env file.")
        raise SystemExit(1)

    print("Fetching live CPCB data (this is a small test batch, not all of India)...\n")
    records = fetch_all_records(max_pages=5, page_size=10)  # ~50 records for now
    print(f"\nFetched {len(records)} raw pollutant readings.\n")

    stations = pivot_records_to_stations(records)
    print(f"Pivoted into {len(stations)} distinct stations.\n")

    compute_aqi_for_all_stations(stations)

    print("=" * 60)
    for station_id, data in stations.items():
        mapped = data["district_id"] or "(not in our district list yet)"
        aqi = data["aqi_result"]["aqi"]
        category = data["aqi_result"]["category"]
        compliant = data["aqi_result"]["is_cpcb_compliant"]
        print(f"{data['station_name']} ({data['city']}, {data['state']}) -> district: {mapped}")
        print(f"  Pollutants measured: {list(data['pollutants'].keys())}")
        print(f"  Computed AQI: {aqi} ({category}) -- CPCB-compliant: {compliant}")
        print()