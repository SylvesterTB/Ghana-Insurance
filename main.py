import requests

def get_place_lat_lng(place_name, district, country, api_key):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    query = f"{place_name}, {district}, {country}"
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
            return latitude, longitude
        else:
            print("No results found")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

# Replace with your actual API key
api_key = 'AIzaSyCKCfkDo_ieuEcQxeRXWJdpCwnyg1TM_qw'

# Replace with your actual place name, district, and country
place_name = 'A.M.E Zion Clinic'
district = 'Offinso North'
country = 'Ghana'

lat_lng = get_place_lat_lng(place_name, district, country, api_key)
if lat_lng:
    print(f"Latitude: {lat_lng[0]}, Longitude: {lat_lng[1]}")
