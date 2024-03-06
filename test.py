import matplotlib.pyplot as plt
from itertools import product
import math
import os

def generate_grid_centers(north, south, west, east, grid_size):
    lat_values = []
    long_values = []

    # Calculate the number of grids in latitude and longitude directions
    num_lat_grids = int((north - south) / grid_size)
    num_long_grids = int((east - west) / grid_size)

    # Iterate through latitude and longitude ranges to calculate center points
    for i in range(num_lat_grids):
        for j in range(num_long_grids):
            # Calculate latitude and longitude of the center of the current grid
            lat_center = south + (i + 0.5) * grid_size
            long_center = west + (j + 0.5) * grid_size

            # Append the center points to the lists
            lat_values.append(lat_center)
            long_values.append(long_center)

    return lat_values, long_values

# San Francisco boundaries
north = 37.8202
south = 37.7095
west = -122.5200
east = -122.3510

grid_size = 0.01  # Adjust the grid size as needed

lat_values, lng_values = generate_grid_centers(north, south, west, east, grid_size)

'''
# Create combinations of coordinates
coordinates = list(product(lat_values, lng_values))

# Extract latitudes and longitudes from coordinates
lats, lngs = zip(*coordinates)

# Plot the coordinates
plt.scatter(lngs, lats)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Coordinate Combinations')

# Plot circles with radius 2000 centered at each point
for lat, lng in coordinates:
    circle = plt.Circle((lng, lat), 1000/111135, color='r', fill=False)
    plt.gca().add_artist(circle)

plt.gca().set_aspect('equal', adjustable='box')

plt.grid(True)
plt.show()
'''
import math

def calculate_center_radius(lat_values, lng_values):
    min_lat, max_lat = min(lat_values), max(lat_values)
    min_lng, max_lng = min(lng_values), max(lng_values)

    center_lat = (min_lat + max_lat) / 2
    center_lng = (min_lng + max_lng) / 2

    # Calculate distance between two points
    def calculate_distance(lat1, lng1, lat2, lng2):
        R = 6371000  # Radius of the Earth in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lng2 - lng1)

        a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    radius = max(calculate_distance(center_lat, center_lng, min_lat, min_lng),
                 calculate_distance(center_lat, center_lng, max_lat, max_lng))

    return center_lat, center_lng, radius

def generate_circle_path(center_lat, center_lng, radius):
    # Construct the circle path string for a given center and radius
    num_points = 5
    circle_points = []
    for i in range(num_points):
        angle = math.radians(float(i) / num_points * 360.0)
        x = center_lng + (radius / 111139) * math.cos(angle)
        y = center_lat + (radius / (111139 * math.cos(math.radians(center_lat)))) * math.sin(angle)
        circle_points.append(f"{y},{x}")

    return '|'.join(circle_points)

def get_static_map_url(circle_paths, center_lat, center_lng, zoom=10):
    # Construct the static map URL with all the circle paths
    circle_str = '|'.join(circle_paths)
    return f"https://maps.googleapis.com/maps/api/staticmap?center={center_lat},{center_lng}&size=600x400&zoom={zoom}&path=color:0x0000ff80|fillcolor:0xFFFF0033|{circle_str}&key={os.getenv('GOOGLE_MAP_API_KEY')}"

# Assuming lat_values and lng_values are already calculated
center_lat, center_lng, _ = calculate_center_radius(lat_values, lng_values)
radius = 900  

# Generate circle paths for all grid centers
circle_paths = [generate_circle_path(lat, lng, radius) for lat, lng in zip(lat_values, lng_values)]

# Generate static map URL
static_map_url = get_static_map_url(circle_paths, center_lat, center_lng)

print("Static Map URL:", static_map_url)

