# The Travelling Team Principal
The Travelling Team Principal is a Formula 1 inspired take on the classic Travelling Salesman Problem. The goal of this Python script is to find the shortest possible route between a set of race tracks, using a nearest neighbor algorithm to solve the Travelling Salesman Problem. The script utilizes the geopy library to calculate the distances between the race tracks using their latitude and longitude coordinates. The result is a list of race tracks that represents the shortest possible route between all the tracks, with the total distance of the route in kilometers.

The script also includes a function to randomly select a starting track and generate a route from that point, as well as a function to find the shortest possible route from all possible starting points.

Overall, The Travelling Team Principal is a useful tool for any Formula 1 enthusiast looking to plan a route for a road trip or simply gain insight into the distances between the various race tracks on the F1 calendar.
# Requirements
Python 3

Clone the repository

Install the required packages: 
```
pip install -r requirements.txt
```

# Usage
To use this script, simply run 
```
python shortest_route.py 
``` 
in your terminal. The script will output the shortest route and total distance.

# Customization
The list of race tracks can be customized by modifying the race_tracks list at the beginning of the script.

The script uses the Nominatim geolocation service to find the latitude and longitude of the race tracks. If you wish to use a different service, you can modify the geocode_track() function accordingly.

# License
This script is licensed under the MIT License.
## Authors

- [Jack David Mullins](https://github.com/jackmullins06)

