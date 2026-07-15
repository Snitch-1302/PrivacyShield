"""
geofencing.py

Geofence membership checks, including a "fuzzy" variant that randomizes
the effective radius slightly so the exact boundary can't be inferred by
repeated probing.
"""

import random

from geopy.distance import geodesic


def check_geofence(user_location, geofence_center, geofence_radius):
    """Return True if user_location is within geofence_radius meters of geofence_center."""
    distance = geodesic(user_location, geofence_center).meters
    return distance <= geofence_radius


def fuzzy_geofence(user_location, geofence_center, base_radius, user_privacy_level):
    """
    Check geofence membership using a radius that's scaled by the user's
    chosen privacy level and randomized slightly each call, so an adversary
    repeatedly probing near the boundary can't pin down its exact location.
    """
    adjusted_radius = base_radius * user_privacy_level
    fuzziness = random.uniform(0.8, 1.2)
    return check_geofence(user_location, geofence_center, adjusted_radius * fuzziness)
