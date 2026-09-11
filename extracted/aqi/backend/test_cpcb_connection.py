"""
STEP 1: Just check the connection works. No database, no saving -- this only
prints what CPCB's live API sends back right now, so you can see real data
before we wire it into the website.

Run this from inside the backend/ folder:
    python test_cpcb_connection.py
"""
import os
import json
import urllib.request
import urllib.parse

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CPCB_API_KEY")
RESOURCE_ID = "3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"  # CPCB's real-time AQI dataset on data.gov.in


def fetch_sample(limit=10):
    """
    Fetch a handful of raw records straight from CPCB, no processing at all.
    The public sample key is capped at 10 records per request -- that's fine
    for this connection test.
    """
    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": limit,
    }
    url = f"https://api.data.gov.in/resource/{RESOURCE_ID}?" + urllib.parse.urlencode(params)

    print(f"Fetching from: {url.replace(API_KEY, '***KEY_HIDDEN***')}\n")

    with urllib.request.urlopen(url, timeout=15) as response:
        data = json.loads(response.read().decode())

    return data


if __name__ == "__main__":
    if not API_KEY:
        print("No CPCB_API_KEY found in your .env file. Add it and try again.")
        raise SystemExit(1)

    result = fetch_sample(limit=10)

    total_available = result.get("total", "unknown")
    records = result.get("records", [])

    print(f"Connection worked. CPCB reports {total_available} total records available.")
    print(f"Got {len(records)} records back (limited by the sample key).\n")

    print("Here's what one real record actually looks like:")
    if records:
        print(json.dumps(records[0], indent=2))
    else:
        print("(No records returned -- see the raw response below to debug why)")
        print(json.dumps(result, indent=2))