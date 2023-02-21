import ssl
import certifi
import random
import folium
import logging
import functools
from folium.features import DivIcon

from tqdm import tqdm
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# Constants

race_tracks = [
    "Bahrain International Circuit", 
    "Jeddah, Corniche Circuit",
    "Albert Park, Melbourne",
    "Baku", 
    "Miami", 
    "Autodromo Enzo e Dino Ferrari", 
    "Circuit de Monaco",
    "Barcelona", 
    "Circuit Gilles Villeneuve", 
    "Red Bull Ring",
    "Hungaroring", 
    "Rte du Circuit 55", 
    "Circuit Zandvoort", 
    "Autodromo Nazionale Monza", 
    "Marina Bay, Singapore",
    "Suzuka Circuit", 
    "Losail International Circuit", 
    "Circuit of the Americas", 
    "Autódromo Hermanos Rodríguez", 
    "Interlagos", 
    "Las Vegas", 
    "Yas Marina Circuit",
    "Silverstone"]

# SSL context for geocoder
CTX = ssl._create_unverified_context(cafile=certifi.where())

# Geocoder
GEOLOCATOR = Nominatim(user_agent="The Travelling Team Principal", timeout=None, ssl_context=CTX)

#Functions
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

    for start_point in tqdm(race_tracks, desc = "Finding shortest route"):
        tracks = race_tracks.copy()
        route = [start_point]
        total_distance = 0
        route, total_distance = nearest_neighbour(start_point, route, total_distance, tracks)

        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_route = route

    return shortest_route, shortest_distance

def create_map(shortest_route):
    # Get the latitude and longitude of each track in the shortest route
    locations = [geocode_track(track) for track in shortest_route]

    # Create a folium map centered at the first track in the route
    map_center = (0,0)
    m = folium.Map(location=map_center, zoom_start=2)

    # Add markers and labels for each track in the route
    prev_location = None
    for i, location in enumerate(locations):
        # Add a marker for the track
        if i == 0:  # Check if it's the first track in the route
            folium.Marker(location=location, popup=shortest_route[i], icon=folium.Icon(color='green')).add_to(m)
        else:
            folium.Marker(location=location, popup=shortest_route[i]).add_to(m)

        # Add a label showing the track name and distance from the previous track
        if prev_location:
            distance = calculate_distance(shortest_route[i-1], shortest_route[i])
            label = "Distance from '{}' to '{}' is {} kilometers".format(shortest_route[i-1], shortest_route[i], round(distance, 2)) 
            folium.PolyLine(locations=[prev_location, location], color='red', tooltip=label).add_to(m)
        prev_location = location

    # Save the map as an HTML file in the current working directory
    m.save('final_route.html')

shortest_route, shortest_distance = find_shortest_route()
print("The optimal route is: {}\n The total distance is {} kilometers".format(shortest_route, round(shortest_distance, 2)))

create_map(shortest_route)