import pandas as pd
import matplotlib.pyplot as plt


def count_facilities(csv_file):
    df = pd.read_csv(csv_file)

    #region facility count
     
    facility_count= {"Greater Accra": 0, "Eastern": 0, "Volta": 0, "Central": 0, "Western": 0, "Ashanti": 0, "Brong Ahafo":0, "Northern": 0, "Upper West":0, "Upper East":0}

    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        region = row['Region']
        
        # Check if the region is in the facility_count dictionary and increment its count
        if region in facility_count:
            facility_count[region] += 1

    return facility_count


csv_file = 'healthFacilities.csv'
total_count = count_facilities( csv_file)
plt.bar(total_count.keys(), total_count.values())
plt.ylabel('Number of Facilities')
plt.xlabel("Regions")
plt.show()
