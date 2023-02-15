import ssl
from tqdm import tqdm
import certifi
import random
import logging
import functools
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

ctx = ssl._create_unverified_context(cafile=certifi.where())
geolocator = Nominatim(user_agent="The Travelling Team Principal", timeout=None, ssl_context=ctx)

race_tracks = ["Bahrain International Circuit", "Jeddah Corniche Circuit ", "Melbourne", "Baku", "Miami", "Imola", "Monaco",
               "Barcelona", "Montreal", "Red Bull Ring", "Silverstone", "Budapest", "Stavelot",
               "Zandvoort", "Monza", "Singapore", "Suzuka", "Doha", "Austin", "Mexico City",
                "Interlagos", "Las Vegas", "Abu Dhabi"]

@functools.lru_cache(maxsize=len(race_tracks))
def geocode_track(track_name):
    try:
        location = geolocator.geocode(track_name)
        if location:
            return round(location.latitude, 5), round(location.longitude, 5)
    except Exception as e:
        logging.warning("Error geocoding {}: {}".format(track_name, str(e)))
    return None

def pick_startpoint():
    tracks = race_tracks.copy()
    start_point = random.choice(tracks)
    route = [start_point]
    total_distance = 0
    print("The starting track is {}".format(start_point))
    route, total_distance = nearest_neighbour(start_point, route, total_distance, tracks)
    print("The route is: {}".format(route))
    print("The total distance is: {} km".format(round(total_distance, 2)))

def calculate_distance(starting_track, next_track):
    start_location = geocode_track(starting_track)
    next_location = geocode_track(next_track)

    if start_location and next_location:
        distance = geodesic(start_location, next_location).kilometers
        return round(distance, 2)
    else:
        return None

total_distance = 0

def nearest_neighbour(start_point, route, total_distance, tracks):
    tracks.remove(start_point)
    shortest_distance = float("inf")
    next_track = None

    for track in tqdm(tracks, desc="Calculating distances"):
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

    for start_point in tqdm(race_tracks, desc="Finding shortest route:"):
        tracks = race_tracks.copy()
        route = [start_point]
        total_distance = 0
        route, total_distance = nearest_neighbour(start_point, route, total_distance, tracks)

        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_route = route

    return shortest_route, shortest_distance


shortest_route, shortest_distance = find_shortest_route()
print("The shortest route is: {}".format(shortest_route))
print("The total distance is: {} km".format(round(shortest_distance, 2)))
