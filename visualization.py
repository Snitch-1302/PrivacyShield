"""
visualization.py

Map and plot rendering for actual vs. cloaked locations, and geofence
visualization.
"""

import folium
import matplotlib.pyplot as plt


def visualize_cloaked_area(actual_location, cloaked_location, radius_km):
    """Render an interactive Folium map showing the actual location, the
    cloaked location, and a circle representing the cloaking radius."""
    m = folium.Map(location=actual_location, zoom_start=15)

    folium.Marker(
        actual_location, popup="Actual Location", icon=folium.Icon(color="red")
    ).add_to(m)
    folium.Marker(
        cloaked_location, popup="Cloaked Location", icon=folium.Icon(color="blue")
    ).add_to(m)
    folium.Circle(
        actual_location, radius=radius_km * 1000, color="blue", fill=True, fill_opacity=0.2
    ).add_to(m)

    return m


def visualize_geofence(user_location, geofence_center, geofence_radius_m):
    """Render a matplotlib plot showing a user's location relative to a geofence."""
    fig, ax = plt.subplots()

    ax.plot(geofence_center[1], geofence_center[0], "ro")
    ax.annotate("Geofence Center", (geofence_center[1], geofence_center[0]))

    ax.plot(user_location[1], user_location[0], "bo")
    ax.annotate("User Location", (user_location[1], user_location[0]))

    circle = plt.Circle(
        (geofence_center[1], geofence_center[0]),
        geofence_radius_m / 111320,
        color="b",
        fill=False,
    )
    ax.add_artist(circle)

    ax.set_xlim([geofence_center[1] - 0.02, geofence_center[1] + 0.02])
    ax.set_ylim([geofence_center[0] - 0.02, geofence_center[0] + 0.02])
    ax.set_aspect("equal")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Geofence Visualization")
    plt.grid(True)
    plt.show()
