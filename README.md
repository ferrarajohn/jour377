# JOUR 370: Data Journalism Final Project: Cafe's VS Gentrification

## Project Description
This repository contains code for retrieving the number of coffee shops in each neighborhood using the Google Places API. The project utilizes techniques for grid creation to overcome the 60 results limit imposed by the API.

## Sample Raw Result JSON
```json
{
    "name": "Spressa",
    "geometry": {
        "location": {
            "lat": 37.7179708,
            "lng": -122.4740931
        },
        "viewport": {
            "northeast": {
                "lat": 37.7192563802915,
                "lng": -122.4728304197085
            },
            "southwest": {
                "lat": 37.7165584197085,
                "lng": -122.4755283802915
            }
        }
    },
    "id": "ChIJo-jzorR9j4ARguQLlDnPPYE",
    "price_level": "",
    "rating": 3.5,
    "types": [
        "cafe",
        "store",
        "food",
        "point_of_interest",
        "establishment"
    ],
    "neighborhood": "Parkmerced"
}
```

## Results
1. `cafes.csv`: Includes cafe names, latitude and longitude location, unique ID, and the neighborhood it belongs to.
2. `cafes_summary.csv`: Aggregated data from `cafes.csv`, counting the number of cafes in each neighborhood.


