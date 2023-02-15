import ssl
import certifi
import random
import geopy.geocoders
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

ctx = ssl._create_unverified_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

geolocator = Nominatim(user_agent="The Travelling Team Principal", timeout=None)

race_tracks = ["Bahrain International Circuit", "Jeddah Corniche Circuit ", "Melbourne", "Baku", "Miami", "Imola", "Monaco",
               "Barcelona", "Montreal", "Red Bull Ring", "Silverstone", "Budapest", "Stavelot",
               "Zandvoort", "Monza", "Singapore", "Suzuka", "Doha", "Austin", "Mexico City",
                "Interlagos", "Las Vegas", "Abu Dhabi"]

def pick_startpoint():    
    start_point = random.choice(race_tracks)
    route = [start_point]
    print("The starting track is {}".format(start_point))

def calculate_distance(starting_track, next_track):
    start_location = round(geolocator.geocode(starting_track).latitude, 5), round(geolocator.geocode(starting_track).longitude, 5)
    next_location = round(geolocator.geocode(next_track).latitude, 5), round(geolocator.geocode(next_track).longitude, 5)
    
    distance = geodesic(start_location, next_location).kilometers

    return round(distance, 2)

pick_startpoint()