"""
differential_privacy.py

Adds calibrated noise to location coordinates using the Laplace mechanism,
and evaluates how robust the resulting obfuscation is against a simple
correlation-attack heuristic.
"""

import numpy as np
from geopy.distance import geodesic


def adaptive_differential_privacy_noise(actual_location, sensitivity):
    """
    Add Laplace-distributed noise to a location, with noise scale set by
    epsilon = 1 / sensitivity. Smaller sensitivity -> larger epsilon budget
    -> less noise; higher sensitivity data gets proportionally more noise.
    """
    epsilon = 1 / sensitivity
    scale = 1 / epsilon

    noise_x = np.random.laplace(0, scale)
    noise_y = np.random.laplace(0, scale)

    return (actual_location[0] + noise_x, actual_location[1] + noise_y)


def evaluate_adversarial_robustness(actual_location, obfuscated_location, threshold_m=500):
    """
    Rough heuristic: if the obfuscated point is farther than `threshold_m`
    meters from the real one, treat it as robust against a naive
    location-correlation attack. This is illustrative, not a rigorous
    privacy guarantee -- a real evaluation would model a specific adversary
    and attack strategy rather than a single distance threshold.
    """
    distance = geodesic(actual_location, obfuscated_location).meters
    if distance > threshold_m:
        return "Robust against correlation attacks"
    return "Vulnerable to correlation attacks"
