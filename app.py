import urllib.request
import json
import time

def get_cafes(api_key, location, radius):
    cafes = []
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type=cafe&key={api_key}"
    while url:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
        cafes.extend(data['results'])
        print(data)
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={data['next_page_token']}&key={api_key}" if 'next_page_token' in data else None
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

# San Francisco boundaries
north = 37.8102
south = 37.7095
west = -123.0566
east = -122.3570

# Size of each grid cell in degrees
lat_step = 0.1
lng_step = 0.1

# Create a grid of latitude and longitude values
lat_values = [south + lat_step * i for i in range(int((north - south) / lat_step) + 1)]
lng_values = [west + lng_step * i for i in range(int((east - west) / lng_step) + 1)]

print(len(lat_values))

# Make a separate API request for each cell in the grid
counts = {}
cell_counter = 0  # Add this line
for i, lat in enumerate(lat_values):
    for j, lng in enumerate(lng_values):
        print(f"Processing cell ({i}, {j})")
        location = f"{lat},{lng}"
        cafes = get_cafes('AIzaSyCKFiVUljZ_RRJpHW7GbSpXYJXE22Zrvf8', location, 500)
        for cafe in cafes:
            location = f"{cafe['geometry']['location']['lat']},{cafe['geometry']['location']['lng']}"
            neighborhood = get_neighborhood('AIzaSyCKFiVUljZ_RRJpHW7GbSpXYJXE22Zrvf8', location)
            if neighborhood:
                if neighborhood in counts:
                    counts[neighborhood] += 1
                else:
                    counts[neighborhood] = 1
        cell_counter += 1  # Increment the counter after each cell
        if cell_counter >= 100:  # Stop after 100 cells
            break
    if cell_counter >= 100:  # Break the outer loop as well
        break

print(counts)
