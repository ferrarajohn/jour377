import os
import json
import urllib.request
import time

def get_cafes(api_key, location, radius):
    cafes = []
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type=cafe&key={api_key}"
    while url:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
        if 'results' in data and data['results']:
            # Extract only required information (name and geometry) from the fetched data
            for result in data['results']:
                cafe_info = {
                    'name': result['name'],
                    'geometry': result['geometry'],
                    'id': result.get('place_id', ''),
                    'price_level': result.get('price_level', ''),
                    'rating': result.get('rating', ''),
                    'types': result.get('types', []),
                }
                cafes.append(cafe_info)
        next_page_token = data.get('next_page_token')
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={api_key}" if next_page_token else None
        time.sleep(2)
    return cafes


def get_neighborhood(api_key, location):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={location}&key={api_key}"
    with urllib.request.urlopen(url) as response:
        address_components = json.loads(response.read())['results'][0]['address_components']
    for component in address_components:
        if 'neighborhood' in component['types']:
            return component['long_name']
    return None


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

import pandas as pd

# Assuming lat_values and lng_values are your lists
lat_series = pd.Series(lat_values)
lng_series = pd.Series(lng_values)

# Now you can use the unique() method
lat_unique_values = lat_series.unique()
lng_unique_values = lng_series.unique()

lat_values = lat_unique_values.tolist()
lng_values = lng_unique_values.tolist()


num_grids = len(lat_values)*len(lng_values)

print(f"There are a total of {num_grids} grids:")

all_cafes = {}  # Dictionary to store cafes in each grid

count = 1

# Used when getting supplimental data 
#lat_values = [37.7850, 37.7875, 37.7900, 37.7925, 37.7950, 37.7975, 37.8000, 37.8025, 37.8050]
#lng_values = [-122.4150, -122.4125, -122.4100, -122.4075, -122.4050, -122.4025, -122.4000, -122.3975, -122.3950]

for i, lat in enumerate(lat_values):
    for j, lng in enumerate(lng_values):
        print(f"{count}/{num_grids}: Processing Point ({lat}, {lng})...")  # Print statement to indicate processing grid
        location = f"{lat},{lng}"
        cafes = get_cafes(os.getenv('GOOGLE_MAP_API_KEY'), location, 200)
        cafes_with_neighborhood = []
        for cafe in cafes:
            cafe_location = f"{cafe['geometry']['location']['lat']},{cafe['geometry']['location']['lng']}"
            neighborhood = get_neighborhood(os.getenv('GOOGLE_MAP_API_KEY'), cafe_location)
            if neighborhood:
                cafe['neighborhood'] = neighborhood
            cafes_with_neighborhood.append(cafe)
        grid_key = f"Grid_{i}_{j}"
        all_cafes[grid_key] = cafes_with_neighborhood
        print(f"Processed {len(cafes_with_neighborhood)} cafes in Grid ({i}, {j})")  # Print statement to indicate cafes processed
        with open('rawdata/all_cafes.json', 'w') as outfile:  # Open file in write mode to overwrite history
            json.dump(all_cafes, outfile, indent=4)
            outfile.write('\n')
        count += 1