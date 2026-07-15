# PrivacyShield

A privacy-preserving location system exploring how to protect a user's exact
location while still allowing useful location-based functionality — nearby
search, geofencing, analytics — without ever exposing raw coordinates.

## What this is

PrivacyShield implements and compares several location-privacy techniques
on the same problem: given a set of real user coordinates, how do you
obscure them enough to prevent tracking or re-identification, while keeping
them useful enough for legitimate features like geofencing or nearby-service
lookup?

Techniques implemented:

- **K-anonymity via DBSCAN clustering** — groups nearby users so any
  individual can't be distinguished from at least *k* others in the same
  cluster
- **Adaptive k-anonymity** — adjusts *k* based on local population density,
  so anonymity requirements scale with how populated an area is
- **Voronoi cloaking** — partitions users into regions and reports a
  cloaked center point instead of an exact location
- **Adaptive differential privacy** — adds calibrated Laplace noise to
  coordinates, with noise scale tied to a configurable sensitivity parameter
- **Fuzzy geofencing** — checks whether a user is inside a zone using a
  randomized radius adjustment, instead of a fixed hard boundary
- **Fernet encryption** — encrypts location data at rest/in transit using
  symmetric encryption

## Tech stack

- Python 3.x
- `scikit-learn` (DBSCAN)
- `scipy` (Voronoi)
- `geopy` (distance calculations)
- `folium` / `matplotlib` (visualization)
- `cryptography` (Fernet encryption)

## Project structure

```text
PrivacyShield/
├── cloaking.py              # DBSCAN & Voronoi-based cloaking
├── differential_privacy.py  # Adaptive DP noise + robustness evaluation
├── geofencing.py             # Fuzzy geofence checks
├── encryption.py              # Fernet encrypt/decrypt
├── external_apis.py           # Population density & nearby-services lookups (illustrative)
├── benchmark.py                # Privacy/usability metrics
├── visualization.py             # Folium/matplotlib map rendering
├── demo.py                       # End-to-end example usage
├── requirements.txt
└── README.md
```


## Setup

```bash
git clone https://github.com/Snitch-1302/PrivacyShield.git
cd PrivacyShield
pip install -r requirements.txt
```

Set your own API key as an environment variable if using the nearby-services lookup:
```bash
export GOOGLE_MAPS_API_KEY="your-key-here"
```

## Running the demo

```bash
python demo.py
```

This runs through: density-based cloaking, adaptive k-anonymity, Voronoi
cloaking, cloaked-area visualization (saved as `cloaked_area_map.html`),
fuzzy geofence checking, differential privacy noise addition, adversarial
robustness evaluation, nearby-service lookup on the obfuscated location,
benchmarking, and location encryption/decryption — using example
coordinates in Chennai.

## Known limitations

- `get_population_density_api()` in `external_apis.py` calls a placeholder
  endpoint — it's illustrative of how a real population-density lookup
  would plug in (e.g. a census or WorldPop API), not a live integration.
- This is a research/demo-oriented project comparing privacy techniques
  side by side, not a hardened production location-privacy system.
- The Voronoi cloaking originally had a region-indexing bug where
  `point_region` values were treated as direct cluster indices — this has
  been fixed to properly group points by their actual assigned Voronoi
  region. See the write-up below for details on what the bug was and why
  it mattered.

## Full write-up

A detailed breakdown of each privacy technique, why they're combined this
way, the Voronoi bug and fix, and honest limitations:
[Hashnode article link]
