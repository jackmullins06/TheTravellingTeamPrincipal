import ssl
import certifi
import random
import folium
import logging
import functools
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# Constants

race_tracks = [
    "Sakhir, Bahrain", "Jeddah, Saudi Arabia", "Melbourne, Australia", "Baku, Azerbaijan", "Miami, Florida", "Imola", " Principality of Monaco",
    "Barcelona, Spain", "Montreal, Canada", "Spielberg, Austria", "Spielberg, Austria", "Mogyoród, Hungaroring, Hungary", "Stavelot, Belgium", "Zandvoort, Netherlands", "Monza, Italy", "Singapore",
    "Suzuka, Japan", "Doha, Qatar", "Austin, Texas", "Mexico City, Mexico", 
    "Interlagos, Sao Paulo, Brazil", "Las Vegas, Nevada", "Abu Dhabi, United Arab Emirates"]

# SSL context for geocoder

CTX = ssl._create_unverified_context(cafile=certifi.where())

# Geocoder

GEOLOCATOR = Nominatim(user_agent="The Travelling Team Principal", timeout=None, ssl_context=CTX)

# Functions

@functools.lru_cache(maxsize=len(race_tracks))
def geocode_track(track_name):
    try:
        location = GEOLOCATOR.geocode(track_name)
        if location:
            return round(location.latitude, 5), round(location.longitude, 5)
    except Exception as e:
        logging.warning("Error geocoding {}: {}".format(track_name, str(e)))
    return None

def calculate_distance(starting_track, next_track):
    start_location = geocode_track(starting_track)
    next_location = geocode_track(next_track)

    if start_location and next_location:
        distance = geodesic(start_location, next_location).kilometers
        return round(distance, 2)
    else:
        return None

def nearest_neighbour(start_point, route, total_distance, tracks):
    tracks.remove(start_point)
    shortest_distance = float("inf")
    next_track = None

    for track in tracks:
        distance = calculate_distance(start_point, track)

        if distance and distance < shortest_distance:
            shortest_distance = distance
            next_track = track

    if next_track:
        total_distance += shortest_distance
        route.append(next_track)
        return nearest_neighbour(next_track, route, total_distance, tracks)
    else:
        return route, total_distance

def find_shortest_route():
    shortest_distance = float("inf")
    shortest_route = None

    for start_point in race_tracks:
        tracks = race_tracks.copy()
        route = [start_point]
        total_distance = 0
        route, total_distance = nearest_neighbour(start_point, route, total_distance, tracks)

        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_route = route

    return shortest_route, shortest_distance

def create_map(map_center, route, zoom_start=4):
    # Create the map object
    route_map = folium.Map(location=map_center, zoom_start=zoom_start)

    # Add markers for each track on the route
    for i, track in enumerate(route):
        location = geocode_track(track)
        if location:
            tooltip = "{}. {}".format(i + 1, track)
            folium.Marker(location=location, tooltip=tooltip).add_to(route_map)

    return route_map


if __name__ == '__main__':
    shortest_route, shortest_distance = find_shortest_route()
    print("The optimal route is: {}\n The total distance is {} kilometers".format(shortest_route, shortest_distance))

    # Create the map
