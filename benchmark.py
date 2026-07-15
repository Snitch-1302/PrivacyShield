"""
benchmark.py

Simple privacy/usability metrics for comparing an obfuscated location
against the actual one.
"""

from geopy.distance import geodesic

from geofencing import check_geofence


def benchmark_performance(
    actual_location, obfuscated_location, cloaked_areas, geofence_center, geofence_radius
):
    """
    Compute basic privacy and usability metrics. `existing_method_*` values
    are illustrative placeholders for comparison -- replace with real
    published baselines if you want a rigorous comparison.
    """
    privacy_distance = geodesic(actual_location, obfuscated_location).meters
    cloaking_entropy = len(cloaked_areas)

    usability_distance = geodesic(actual_location, geofence_center).meters
    within_geofence = check_geofence(actual_location, geofence_center, geofence_radius)

    return {
        "privacy_distance": privacy_distance,
        "cloaking_entropy": cloaking_entropy,
        "usability_distance": usability_distance,
        "within_geofence": within_geofence,
        "existing_method_privacy_distance": 1000,  # placeholder baseline
        "existing_method_usability_distance": 500,  # placeholder baseline
    }
