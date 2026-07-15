"""
cloaking.py

Location cloaking techniques for k-anonymity:
- Density-based clustering (DBSCAN) cloaking
- Adaptive k-anonymity based on local population density
- Voronoi-based cloaking
"""

import math
import random

import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial import Voronoi


def haversine(lat1, lon1, lat2, lon2):
    """Great-circle distance between two lat/lon points, in kilometers."""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def generate_cloaked_area_haversine(actual_location, radius):
    """Generate a random point within `radius` km of actual_location."""
    R = 6371
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, radius)

    lat1 = math.radians(actual_location[0])
    lon1 = math.radians(actual_location[1])

    lat2 = math.asin(
        math.sin(lat1) * math.cos(distance / R)
        + math.cos(lat1) * math.sin(distance / R) * math.cos(angle)
    )
    lon2 = lon1 + math.atan2(
        math.sin(angle) * math.sin(distance / R) * math.cos(lat1),
        math.cos(distance / R) - math.sin(lat1) * math.sin(lat2),
    )

    return (math.degrees(lat2), math.degrees(lon2))


def density_based_cloaking(user_locations, k, radius):
    """
    Cluster user locations with DBSCAN and generate a cloaked area for each
    cluster that has at least k members. Clusters smaller than k (or noise
    points, label == -1) are dropped rather than force-anonymized.
    """
    locations = np.array(user_locations)
    db = DBSCAN(eps=radius / 111320, min_samples=k).fit(locations)
    labels = db.labels_

    cloaked_areas = []
    for label in set(labels):
        if label == -1:
            continue  # noise points, not enough neighbors for k-anonymity
        cluster = locations[labels == label]
        if len(cluster) >= k:
            center = cluster.mean(axis=0)
            cloaked_areas.append(generate_cloaked_area_haversine(center, radius))

    return cloaked_areas


def estimate_population_density(location, population_data):
    """Look up population density for a location from a provided dataset."""
    return population_data.get(location, 1000)  # default if no data available


def adaptive_k_anonymity(user_locations, base_k, radius, population_data):
    """
    Group locations into clusters, requiring a larger k in denser areas
    (denser areas can support tighter grouping without weakening anonymity).
    """
    clusters = []
    for location in user_locations:
        density = estimate_population_density(location, population_data)
        k = base_k + (density // 1000)

        added = False
        for cluster in clusters:
            if len(cluster) < k:
                cluster.append(location)
                added = True
                break
        if not added:
            clusters.append([location])

    cloaked_areas = []
    for cluster in clusters:
        center = (
            sum(loc[0] for loc in cluster) / len(cluster),
            sum(loc[1] for loc in cluster) / len(cluster),
        )
        cloaked_areas.append(generate_cloaked_area_haversine(center, radius))

    return cloaked_areas


def voronoi_cloaking(user_locations, k, cloak_radius_km=0.5):
    """
    Partition users into Voronoi regions and report a cloaked center point
    per region instead of individual coordinates.

    NOTE ON A BUG WE FIXED: the original version indexed `vor.point_region`
    as if position in that array corresponded 1:1 to a region grouping,
    which is not how scipy's Voronoi output works -- point_region[i] gives
    the region *index* that point i belongs to, not a cluster id you can
    iterate over directly. This version groups points correctly by their
    actual assigned region id.
    """
    if len(user_locations) < 4:
        # Voronoi diagrams need at least 4 non-collinear points in 2D
        return []

    points = np.array(user_locations)
    vor = Voronoi(points)

    # Group point INDICES by the region id they actually belong to
    region_to_points = {}
    for point_idx, region_id in enumerate(vor.point_region):
        region_to_points.setdefault(region_id, []).append(point_idx)

    cloaked_areas = []
    for point_indices in region_to_points.values():
        if len(point_indices) >= k:
            cluster = points[point_indices]
            center = (cluster[:, 0].mean(), cluster[:, 1].mean())
            cloaked_areas.append(generate_cloaked_area_haversine(center, cloak_radius_km))

    return cloaked_areas
