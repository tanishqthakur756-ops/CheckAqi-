"""
Seed script — populates the database with sample stations, daily readings
(Contract A), and district rollups (Contract B).

This allows the API and frontend to be developed against real data shapes
even before the ingestion pipeline is running.

Usage:
    python -m app.seed_data
"""

import random
from datetime import date, datetime, timedelta

from .db import init_db, SessionLocal
from .models import Station, DailyReading, DistrictRollup
from .analytics.aqi_calculator import compute_station_aqi
from .analytics.utils import get_imd_season, safe_mean, safe_max


# Sample stations mapped to districts
SAMPLE_STATIONS = [
    {"station_id": "DL001", "station_name": "Central Delhi CPCB", "district_id": "dl_delhi",
     "latitude": 28.6139, "longitude": 77.2090, "source": "CPCB"},
    {"station_id": "DL002", "station_name": "East Delhi CPCB", "district_id": "dl_east",
     "latitude": 28.5749, "longitude": 77.2820, "source": "CPCB"},
    {"station_id": "UP001", "station_name": "Lucknow CPCB", "district_id": "up_lucknow",
     "latitude": 26.8499, "longitude": 80.9498, "source": "CPCB"},
    {"station_id": "UP002", "station_name": "Kanpur CPCB", "district_id": "up_kanpur",
     "latitude": 26.4292, "longitude": 80.3342, "source": "CPCB"},
    {"station_id": "MH001", "station_name": "Mumbai CPCB", "district_id": "mh_mumbai",
     "latitude": 19.0760, "longitude": 72.8777, "source": "CPCB"},
    {"station_id": "MH002", "station_name": "Pune CPCB", "district_id": "mh_pune",
     "latitude": 18.5204, "longitude": 73.8567, "source": "CPCB"},
    {"station_id": "TN001", "station_name": "Chennai CPCB", "district_id": "tn_chennai",
     "latitude": 13.0827, "longitude": 80.2747, "source": "CPCB"},
    {"station_id": "KA001", "station_name": "Bengaluru CPCB", "district_id": "ka_bengaluru",
     "latitude": 12.9716, "longitude": 77.5946, "source": "CPCB"},
    {"station_id": "WB001", "station_name": "Kolkata CPCB", "district_id": "wb_kolkata",
     "latitude": 22.5726, "longitude": 88.3639, "source": "CPCB"},
    {"station_id": "GJ001", "station_name": "Ahmedabad CPCB", "district_id": "gj_ahmedabad",
     "latitude": 23.2156, "longitude": 72.5563, "source": "CPCB"},
    {"station_id": "RJ001", "station_name": "Jaipur CPCB", "district_id": "rj_jaipur",
     "latitude": 26.9124, "longitude": 75.7873, "source": "CPCB"},
    {"station_id": "TG001", "station_name": "Hyderabad CPCB", "district_id": "tg_hyderabad",
     "latitude": 17.3610, "longitude": 78.4780, "source": "CPCB"},
]


def _parse_date(date_str: str) -> date:
    """Convert a 'YYYY-MM-DD' string to a date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def generate_daily_readings(start_date: date, end_date: date) -> list[dict]:
    """
    Generate synthetic daily readings for all sample stations.

    FIX: previously this picked a random target AQI and reverse-derived
    pollutant concentrations from it (aqi*0.6 etc.), importing
    compute_station_aqi but never actually calling it -- so the AQI
    calculator was never exercised by the seed data at all. Now we generate
    plausible pollutant concentrations first and run them through the real
    calculator, the same way live ingestion will.
    """
    readings = []
    current = start_date

    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        season = get_imd_season(date_str)

        for station in SAMPLE_STATIONS:
            # Seasonal pollutant concentration ranges (mu g/m3), winter worst
            if season == "winter":
                pm2_5 = round(random.uniform(90, 280), 1)
            elif season == "summer":
                pm2_5 = round(random.uniform(60, 160), 1)
            elif season == "monsoon":
                pm2_5 = round(random.uniform(15, 70), 1)
            else:  # post_monsoon
                pm2_5 = round(random.uniform(50, 150), 1)

            pm10 = round(pm2_5 * random.uniform(1.3, 1.8), 1)
            no2 = round(random.uniform(15, 90) * (1.4 if season == "winter" else 1.0), 1)

            aqi_result = compute_station_aqi({"pm2_5": pm2_5, "pm10": pm10, "no2": no2})

            # Weather varies by season
            if season == "winter":
                temp = round(random.uniform(10, 25), 1)
                rainfall = 0.0
            elif season == "summer":
                temp = round(random.uniform(28, 45), 1)
                rainfall = 0.0
            elif season == "monsoon":
                temp = round(random.uniform(22, 32), 1)
                rainfall = round(random.uniform(0, 50), 1)
            else:
                temp = round(random.uniform(18, 30), 1)
                rainfall = round(random.uniform(0, 10), 1)

            # Wind tends to be higher in monsoon (helps ventilate pollution)
            wind_speed = round(random.uniform(12, 28) if season == "monsoon" else random.uniform(4, 14), 1)

            readings.append({
                "station_id": station["station_id"],
                "district_id": station["district_id"],
                "date": date_str,
                "aqi": aqi_result["aqi"],
                "pm2_5": pm2_5,
                "pm10": pm10,
                "no2": no2,
                "temperature": temp,
                "rainfall_mm": rainfall,
                "wind_speed_kmh": wind_speed,
                "data_type": "observed",
                "source": "CPCB",
            })

        current += timedelta(days=1)

    return readings


def generate_rollups_from_readings(readings: list[dict]) -> list[dict]:
    """
    FIX: rollups were previously generated as a second, entirely independent
    random dataset, so daily_readings and district_rollups never agreed with
    each other for the same dates. Now rollups are derived BY AVERAGING the
    actual readings above, matching how the real pipeline (recompute_district_
    rollups) works.
    """
    by_district_date: dict[tuple[str, str], list[dict]] = {}
    for r in readings:
        key = (r["district_id"], r["date"])
        by_district_date.setdefault(key, []).append(r)

    rollups = []
    for (district_id, date_str), rows in by_district_date.items():
        aqi_vals = [r["aqi"] for r in rows if r["aqi"] is not None]
        rollups.append({
            "district_id": district_id,
            "date": date_str,
            "avg_aqi": safe_mean(aqi_vals),
            "max_aqi": safe_max(aqi_vals),
            "avg_temp": safe_mean([r["temperature"] for r in rows]),
            "avg_rainfall": safe_mean([r["rainfall_mm"] for r in rows]),
            "avg_wind": safe_mean([r["wind_speed_kmh"] for r in rows]),
            "season": get_imd_season(date_str),
            "station_count": len(rows),
            "coverage_type": "station",
        })
    return rollups


def seed_database():
    """Populate the database with sample data."""
    # Initialize schema + seed districts
    init_db()

    db = SessionLocal()

    try:
        # Clear existing sample data
        db.query(DailyReading).delete()
        db.query(DistrictRollup).delete()
        db.query(Station).delete()
        db.commit()

        # Insert sample stations
        for station_data in SAMPLE_STATIONS:
            station = Station(**station_data)
            db.add(station)
        db.commit()
        print(f"Inserted {len(SAMPLE_STATIONS)} sample stations.")

        # Generate readings for the past 365 days
        today = date.today()
        start_date = today - timedelta(days=365)

        readings = generate_daily_readings(start_date, today)
        for r in readings:
            reading = DailyReading(
                station_id=r["station_id"],
                date=_parse_date(r["date"]),
                aqi=r["aqi"],
                pm2_5=r["pm2_5"],
                pm10=r["pm10"],
                no2=r["no2"],
                temperature=r["temperature"],
                rainfall_mm=r["rainfall_mm"],
                wind_speed_kmh=r["wind_speed_kmh"],
                data_type=r["data_type"],
                source=r["source"],
            )
            db.add(reading)
        db.commit()
        print(f"Inserted {len(readings)} daily readings (Contract A).")

        # FIX: rollups are now derived FROM the readings just inserted above,
        # instead of being a second independent random dataset.
        rollups = generate_rollups_from_readings(readings)
        for r in rollups:
            rollup = DistrictRollup(
                district_id=r["district_id"],
                date=_parse_date(r["date"]),
                avg_aqi=r["avg_aqi"],
                max_aqi=r["max_aqi"],
                avg_temp=r["avg_temp"],
                avg_rainfall=r["avg_rainfall"],
                avg_wind=r["avg_wind"],
                season=r["season"],
                station_count=r["station_count"],
                coverage_type=r["coverage_type"],
            )
            db.add(rollup)
        db.commit()
        print(f"Inserted {len(rollups)} district rollups (Contract B), derived from readings.")

        print("\nDatabase seeded successfully!")
        print(f"  - {len(SAMPLE_STATIONS)} stations")
        print(f"  - {len(readings)} daily readings")
        print(f"  - {len(rollups)} district rollups")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
