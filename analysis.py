import json
import csv

def parse_multiple_json_to_csv(input_files, output_file):
    merged_data = {}

    # Merge data from all JSON files into a single dictionary
    for input_file in input_files:
        with open(input_file, 'r') as json_file:
            data = json.load(json_file)
            for grid, places in data.items():
                for place in places:
                    place_id = place.get('id', '')  # Assuming 'id' is the key for deduplication
                    if place_id not in merged_data:
                        merged_data[place_id] = place

    # Sort data based on neighborhood
    sorted_data = sorted(merged_data.values(), key=lambda x: x.get('neighborhood', ''))

    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ID', 'Place Name', 'Neighborhood'])  # Added 'ID' column to CSV

        for place in sorted_data:
            place_id = place.get('id', '')
            place_name = place.get('name', '')
            neighborhood = place.get('neighborhood', '')
            writer.writerow([place_id, place_name, neighborhood])

if __name__ == "__main__":
    input_files = ["all_cafes.json", "all_cafes_sup.json"]  # List of JSON file paths
    output_file = "cafes.csv"  # Change this to your desired CSV file path
    parse_multiple_json_to_csv(input_files, output_file)
