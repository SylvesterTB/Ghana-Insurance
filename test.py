import pandas as pd
import requests
from geopy.distance import geodesic
import csv
import math

def get_place_lat_lng(place_name, district, country, region, api_key):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    query = f"{place_name}, {district}, {country}, {region}"
    params = {
        'query': query,
        'key': api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            place = results[0]  # Get the first result
    
            location = place['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            business_status = place.get('business_status', 'N/A')

            return latitude, longitude, business_status
        else:
            return None
    else:
        return None

def compare_coordinates(csv_file, api_key, threshold=0.5, limit=1000):
    df = pd.read_csv(csv_file)
    
    # Limit to the first `limit` rows
    df = df.head(limit)
    results = []
    for index, row in df.iterrows():
        csv_lat = row['latitude']
        csv_lng = row['longitude']
        facility_name = row['FacilityName']
        district = row['District']
        country = row['Region']

        if math.isnan(csv_lat) or math.isnan(csv_lng):
            print(f"Invalid CSV coordinates for {facility_name}. Skipping.")
            results.append([facility_name, csv_lat, csv_lng, 'N/A', 'N/A', 'N/A', 'false'])
            continue

        google_coords = get_place_lat_lng(facility_name, district, country, '', api_key)
        
        if google_coords:
            google_lat, google_lng, business_status = google_coords
            csv_coords = (csv_lat, csv_lng)
            google_coords = (google_lat, google_lng)
            distance = geodesic(csv_coords, google_coords).kilometers
            
            is_accurate = 'true' if distance <= threshold else 'false'
            if business_status == "OPERATIONAL":
             results.append([
                facility_name,
                csv_lat,
                csv_lng,
                google_lat,
                google_lng,
                business_status,
                is_accurate
            ])
            elif business_status == "CLOSED_PERMANENTLY":
                 results.append([
                facility_name,
                csv_lat,
                csv_lng,
                google_lat,
                google_lng,
                "CLOSED_PERMANENTLY",
                is_accurate
                ])
            else:
              results.append([
                facility_name,
                csv_lat,
                csv_lng,
                google_lat,
                google_lng,
                "NO DATA",
                is_accurate

])
        else:
            results.append([
                facility_name,
                csv_lat,
                csv_lng,
                'N/A',
                'N/A',
                'NO DATA',
                'false'
            ])
    output_file = 'output4.csv'
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['FacilityName', 'CSV_Latitude', 'CSV_Longitude', 'Google_Latitude', 'Google_Longitude', 'Business_Status', 'Is_Accurate'])
        writer.writerows(results)
    
    print(f"Results have been written to {output_file}")


    
api_key = 'AIzaSyCKCfkDo_ieuEcQxeRXWJdpCwnyg1TM_qw'


csv_file = 'healthFacilities.csv'

compare_coordinates(csv_file, api_key)

