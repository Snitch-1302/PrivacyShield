"""
demo.py

End-to-end walkthrough of every technique in PrivacyShield, using example
coordinates in Chennai. Run with: python demo.py
"""

from cloaking import (
    density_based_cloaking,
    adaptive_k_anonymity,
    voronoi_cloaking,
    generate_cloaked_area_haversine,
)
from differential_privacy import (
    adaptive_differential_privacy_noise,
    evaluate_adversarial_robustness,
)
from geofencing import fuzzy_geofence
from encryption import generate_key, encrypt_location_data, decrypt_location_data
from external_apis import fetch_nearby_services
from benchmark import benchmark_performance
from visualization import visualize_cloaked_area, visualize_geofence


def main():
    # Example coordinates in Chennai
    actual_location = (13.0827, 80.2707)
    radius = 0.5  # km
    user_locations = [
        (13.0827, 80.2707),
        (13.0838, 80.2710),
        (13.0848, 80.2720),
        (13.0858, 80.2730),
    ]
    base_k = 2
    population_data = {
        (13.0827, 80.2707): 5000,
        (13.0838, 80.2710): 4500,
        (13.0848, 80.2720): 4000,
        (13.0858, 80.2730): 3500,
    }

    # --- K-anonymity via density-based clustering ---
    cloaked_areas = density_based_cloaking(user_locations, base_k, radius)
    print("Density-based cloaked areas:", cloaked_areas)

    # --- Adaptive k-anonymity ---
    cloaked_areas_adaptive = adaptive_k_anonymity(user_locations, base_k, radius, population_data)
    print("Adaptive k-anonymity cloaked areas:", cloaked_areas_adaptive)

    # --- Voronoi cloaking ---
    cloaked_areas_voronoi = voronoi_cloaking(user_locations, k=1)
    print("Voronoi cloaked areas:", cloaked_areas_voronoi)

    # --- Visualize a single cloaked point ---
    cloaked_location = generate_cloaked_area_haversine(actual_location, radius)
    map_cloaked_area = visualize_cloaked_area(actual_location, cloaked_location, radius)
    map_cloaked_area.save("cloaked_area_map.html")
    print("Saved map to cloaked_area_map.html")

    # --- Fuzzy geofencing ---
    geofence_center = (13.0827, 80.2707)
    base_radius = 500  # meters
    user_privacy_level = 1.5
    user_location = (13.0838, 80.2710)

    inside = fuzzy_geofence(user_location, geofence_center, base_radius, user_privacy_level)
    print("User is inside the fuzzy geofence." if inside else "User is outside the fuzzy geofence.")
    visualize_geofence(user_location, geofence_center, base_radius * user_privacy_level)

    # --- Differential privacy ---
    sensitivity = 0.05
    obfuscated_location = adaptive_differential_privacy_noise(actual_location, sensitivity)
    print("Obfuscated location (DP noise):", obfuscated_location)

    robustness = evaluate_adversarial_robustness(actual_location, obfuscated_location)
    print("Adversarial robustness:", robustness)

    # --- Nearby services on the OBFUSCATED location, not the real one ---
    nearby_services = fetch_nearby_services(obfuscated_location)
    print("Nearby services:", nearby_services)

    # --- Benchmark ---
    metrics = benchmark_performance(
        actual_location, obfuscated_location, cloaked_areas, geofence_center, base_radius
    )
    print("Benchmark metrics:", metrics)

    # --- Encryption ---
    key = generate_key()
    encrypted_location = encrypt_location_data(actual_location, key)
    print("Encrypted location:", encrypted_location)

    decrypted_location = decrypt_location_data(encrypted_location, key)
    print("Decrypted location:", decrypted_location)


if __name__ == "__main__":
    main()
