import pickle
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path
import streamlit_authenticator as stauth

names = ['Sylvester Broich', 'Dimitri Missoh']
usernames = ['sbroich', 'dmissoh']

file_path = Path(__file__).parent/"hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'sales_dashboard', 'abcdef', cookie_expiry_days=7)


name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:



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
        st.header(""" A brief description:""")
        st.write(""" The data in this app is regarding health facilities in Ghana, the full csv file is viewable below. The file contained longitude and latitude and the goal was to make a program that validated those coordinates by using Google Places API. Displayed below are graphs containing the amount of health facilities per region and how many are still Operational, unkown, or closed permanently. After that there is a map containing points of every health facility with valid coordinates.""" )
        
        csv_file = 'healthFacilities.csv'
        
        df = pd.read_csv(csv_file)
        st.subheader("Health Facilities Data")
        st.dataframe(df)

        total_count = count_facilities(csv_file)
        status_count = Operational_counter("total_data.csv")
        
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
        df = pd.read_csv('total_data.csv')
        
        # Filter for rows where Is_Accurate is true
        accurate_df = df[df['Is_Accurate'] == True]

        # Display the map using Streamlit   
        st.map(accurate_df, latitude = "Latitude", longitude="Longitude")
     
    if __name__ == "__main__":
        main()


# pie chart, deployment, password protection, read csv,  decoration later, upload data