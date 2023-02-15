import ssl
import certifi
import geopy.geocoders
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

ctx = ssl._create_unverified_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

geolocator = Nominatim(user_agent="The Travelling Team Principal", timeout=None)

def calculate_distance(starting_track, next_track):
    start_location = round(geolocator.geocode(starting_track).latitude, 5), round(geolocator.geocode(starting_track).longitude, 5)
    next_location = round(geolocator.geocode(next_track).latitude, 5), round(geolocator.geocode(next_track).longitude, 5)
    
    distance = geodesic(start_location, next_location).kilometers

    return round(distance, 2)



print(calculate_distance("New York", "Los Angeles")) 