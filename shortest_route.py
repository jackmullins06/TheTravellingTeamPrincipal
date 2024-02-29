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
import argparse

class RaceRouteOptimizer:
    def __init__(self):
        # Constants
        self.race_tracks = []
        # SSL context for geocoder
        self.CTX = ssl._create_unverified_context(cafile=certifi.where())
        # Geocoder
        self.GEOLOCATOR = Nominatim(user_agent="The Travelling Team Principal", timeout=None, ssl_context=self.CTX)
    
    """Load race tracks into the array from an external text file."""
    def load_race_tracks(self):
        try:
            with open('racetracks.txt', 'r') as racetracks:
                self.race_tracks.extend(line.strip() for line in racetracks)
        except FileNotFoundError:
            print("Error: racetracks.txt not found or could not be opened.")

    @functools.lru_cache(maxsize=None)
    def geocode_track(self, track_name):
        try:
            location = self.GEOLOCATOR.geocode(track_name)
            if location:
                return round(location.latitude, 5), round(location.longitude, 5)
        except Exception as e:
            logging.warning("Error geocoding {}: {}".format(track_name, str(e)))
        return None
    
    def calculate_distance(self, starting_track, next_track):
        start_location = self.geocode_track(starting_track)
        next_location = self.geocode_track(next_track)

        if start_location and next_location:
            distance = geodesic(start_location, next_location).kilometers
            return round(distance, 2)
        else:
            return None
    
    def nearest_neighbour(self, start_point, route, total_distance, tracks):
        tracks.remove(start_point)
        shortest_distance = float("inf")
        next_track = None

        for track in tracks:
            distance = self.calculate_distance(start_point, track)

            if distance and distance < shortest_distance:
                shortest_distance = distance
                next_track = track

        if next_track:
            total_distance += shortest_distance
            route.append(next_track)
            return self.nearest_neighbour(next_track, route, total_distance, tracks)
        else:
            return route, total_distance
    
    def find_shortest_route(self, start_point=None):
        shortest_distance = float("inf")
        shortest_route = None

        if start_point:
            tracks = self.race_tracks.copy()
            route = [start_point]
            total_distance = 0
            route, total_distance = self.nearest_neighbour(start_point, route, total_distance, tracks)

            if total_distance < shortest_distance:
                shortest_distance = total_distance
                shortest_route = route
        else:
            for start_point in tqdm(self.race_tracks, desc="Finding shortest route"):
                tracks = self.race_tracks.copy()
                route = [start_point]
                total_distance = 0
                route, total_distance = self.nearest_neighbour(start_point, route, total_distance, tracks)

                if total_distance < shortest_distance:
                    shortest_distance = total_distance
                    shortest_route = route

        return shortest_route, shortest_distance
    
    def create_map(self, shortest_route):
        # Get the latitude and longitude of each track in the shortest route
        locations = [self.geocode_track(track) for track in shortest_route]

        # Create a folium map centered at the first track in the route
        map_center = (0, 0)
        m = folium.Map(location=map_center, zoom_start=2)

        # Add markers and labels for each track in the route
        prev_location = None
        for i, location in enumerate(locations):
            # Add a marker for the track
            if i == 0:  # Check if it's the first track in the route
                folium.Marker(location=location, popup=shortest_route[i], icon=folium.Icon(color='green')).add_to(m)
            elif i == len(locations) - 1: 
                folium.Marker(location=location, popup=shortest_route[i], icon=folium.Icon(color='red')).add_to(m)
            else:
                folium.Marker(location=location, popup=shortest_route[i]).add_to(m)

            # Add a label showing the track name and distance from the previous track
            if prev_location:
                distance = self.calculate_distance(shortest_route[i-1], shortest_route[i])
                label = "Distance from '{}' to '{}' is {} kilometers".format(shortest_route[i-1], shortest_route[i], round(distance, 2))
                folium.PolyLine(locations=[prev_location, location], color='red', tooltip=label).add_to(m)
            prev_location = location

        # Save the map as an HTML file in the current working directory
        m.save('final_route.html')

    def optimize_route(self, start_point=None):
        shortest_route, shortest_distance = self.find_shortest_route(start_point)
        print("The optimal route is: {}\n The total distance is {} kilometers".format(shortest_route, round(shortest_distance, 2)))

        self.create_map(shortest_route)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Race Route Optimizer")
    parser.add_argument("--start-point", type=str, help="Specify a start point for the route optimization.")
    args = parser.parse_args()

    optimizer = RaceRouteOptimizer()
    optimizer.load_race_tracks()
    
    # Use the command-line argument as the start point
    start_point = args.start_point
    
    optimizer.optimize_route(start_point)