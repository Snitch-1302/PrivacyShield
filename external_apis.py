"""
external_apis.py

Illustrative integrations with external data sources. These are placeholders
showing how real population-density and places APIs would plug into the
system -- they are NOT live integrations. Swap in a real provider (e.g. a
census/WorldPop API for population density, Google Places for nearby
services) before using this in anything beyond a demo.
"""

import os

import requests


def get_population_density_api(location):
    """
    PLACEHOLDER: illustrates how a real population-density lookup would
    plug in. `api.example.com` is not a real, reachable API -- replace this
    with an actual provider (e.g. WorldPop, national census data APIs).
    """
    api_url = f"https://api.example.com/population_density?lat={location[0]}&lon={location[1]}"
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return response.json()["density"]
    except requests.RequestException:
        pass
    return 1000  # fallback default


def fetch_nearby_services(obfuscated_location, api_key=None):
    """
    Fetch nearby services using the Google Places API, based on an
    (already-obfuscated) location -- never pass a raw, un-cloaked user
    location to a third-party API.

    Reads the API key from the GOOGLE_MAPS_API_KEY environment variable if
    not passed explicitly. Never hardcode real API keys in source code.
    """
    api_key = api_key or os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return {"error_message": "No API key configured.", "results": []}

    url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={obfuscated_location[0]},{obfuscated_location[1]}"
        f"&radius=1500&key={api_key}"
    )
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return response.json()
    return {"error_message": "Failed to fetch nearby services.", "results": []}
