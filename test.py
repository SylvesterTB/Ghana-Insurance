import pandas as pd
import requests
from geopy.distance import geodesic

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
            place = results[0] 
           # print(place) # Get the first result
    
            location = place['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            # formatted address and buisness status
            business_status = place.get('business_status', 'N/A')
            formatted_address = place.get('formatted_address', 'N/A')
            print( business_status, formatted_address)

            return latitude, longitude,  
        else:
            print("No results found")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

def compare_coordinates(csv_file, api_key, threshold=0.5):
    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        csv_lat = row['Latitude']
        csv_lng = row['Longitude']
        facility_name = row['FacilityName']
        district = row['District']
        country = row['Region']

        google_coords = get_place_lat_lng(facility_name, district, country, '', api_key)
        
        if google_coords:
            google_lat, google_lng = google_coords
            csv_coords = (csv_lat, csv_lng)
            google_coords = (google_lat, google_lng)
            distance = geodesic(csv_coords, google_coords).kilometers
            
            print(f"Facility: {facility_name}, Distance: {distance:.2f} km")
            
            if distance <= threshold:
                print(f"Coordinates for {facility_name} are accurate.")
            else:
                print(f"Coordinates for {facility_name} are not accurate.")
        else:
            print(f"Google could not find coordinates for {facility_name}.")

# Replace with your actual API key
api_key = 'AIzaSyCKCfkDo_ieuEcQxeRXWJdpCwnyg1TM_qw'

# Replace with your actual CSV file path
csv_file = 'healthFacilities.csv'

# Call the function to compare coordinates
compare_coordinates(csv_file, api_key)
