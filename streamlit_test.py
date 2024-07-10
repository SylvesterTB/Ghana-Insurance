import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def count_facilities(csv_file):
    df = pd.read_csv(csv_file)

    # Region facility count
    facility_count = {
        "Greater Accra": 0, "Eastern": 0, "Volta": 0, "Central": 0, 
        "Western": 0, "Ashanti": 0, "Brong Ahafo": 0, "Northern": 0, 
        "Upper West": 0, "Upper East": 0
    }

    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        region = row['Region']
        
        # Check if the region is in the facility_count dictionary and increment its count
        if region in facility_count:
            facility_count[region] += 1

    return facility_count

def Operational_counter(csv_file):
    df = pd.read_csv(csv_file)
    Operational_count = {
        "OPERATIONAL": 0, "NO DATA": 0, "CLOSED_PERMANENTLY": 0
    }

    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        status = row['Business_Status']
        
        if status in Operational_count:
            Operational_count[status] += 1

    return Operational_count

def main():
    st.title("Health Facilities Analysis")
    
    csv_file = 'healthFacilities.csv'
    total_count = count_facilities(csv_file)
    status_count = Operational_counter("output4.csv")
    
    # Convert the dictionaries to DataFrames
    df_total_count = pd.DataFrame(list(total_count.items()), columns=['Region', 'Number of Facilities'])
    df_status_count = pd.DataFrame(list(status_count.items()), columns=['Business_Status', 'Number Open'])

    # Display the bar chart for number of facilities by region
    st.subheader("Number of Facilities by Region")
    st.bar_chart(df_total_count.set_index('Region'))

    # Display the pie chart for business status
    st.subheader("Distribution of Business Status")
    labels = df_status_count['Business_Status']
    sizes = df_status_count['Number Open']
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

    # Load the CSV file for mapping
  

    # Load the CSV file for mapping 
    df = pd.read_csv('output.csv')
     
    # Filter for rows where Is_Accurate is true
    accurate_df = df[df['Is_Accurate'] == True]

    # Display the map using Streamlit  
    st.map(accurate_df, latitude = "Latitude", longitude="Longitude")
  
if __name__ == "__main__":
    main()


# pie chart, deployment, password protection, read csv,  decoration later, upload data