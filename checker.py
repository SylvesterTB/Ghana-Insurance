import pandas as pd

def find_missing_coordinates(csv_file):
    df = pd.read_csv(csv_file)

    # Check for NaN values in Latitude and Longitude columns
    missing_coords = df[df[['latitude', 'longitude']].isnull().any(axis=1)]
    
    # Display rows with missing coordinates
    if not missing_coords.empty:
        print("Rows with missing latitude or longitude:")
        print(missing_coords)
    else:
        print("No missing coordinates found.")

csv_file = 'healthFacilities.csv'
find_missing_coordinates(csv_file)
