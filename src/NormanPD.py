import streamlit as st
import pandas as pd
import argparse
import os, datetime, sys
import extraction, augmentation


# Set the page configuration
st.set_page_config(layout="wide", page_title="Norman Police Department App", page_icon="🚔")
st.title('Incident Summaries in Norman, OK')

# Assign a default value to the date picker state
today = datetime.datetime.now()
min_date = datetime.datetime(today.year, 12, 1) if (today.month == 1) else datetime.datetime(today.year, today.month - 1, 1)
max_date = datetime.datetime(today.year, today.month, today.day) if (today.day < 3) else datetime.datetime(today.year, today.month, today.day - 2)

if "incident_date_range" not in st.session_state:
    st.session_state.incident_date_range = [min_date, max_date]


# Download and augment the incident data for the selected dates
@st.cache_data
def download_pdfs(all_dates):
    # Delete the old augmented file if it exists
    try:
        os.remove("../resources/normanpd_raw.db")
        os.remove("../resources/normanpd_augmented.csv")
    except FileNotFoundError:
        pass

    # Initialize the database connection
    db = None

    # Iterate through each url and extract the raw incident data
    for date in all_dates:
        # Create the url for each selected date
        ## Example URL: https://www.normanok.gov/sites/default/files/documents/YYYY-MM/YYYY-MM-DD_daily_incident_summary.pdf
        url = "https://www.normanok.gov/sites/default/files/documents/" + date.strftime("%Y-%m") + "/" + date.strftime("%Y-%m-%d") + "_daily_incident_summary.pdf"

        # Download data from the url
        incident_data = extraction.fetchincidents(url)

        # Extract data
        incidents = extraction.extractincidents(incident_data)

        # Create new database
        db = extraction.createdb("normanpd_raw")

        # Insert the extracted raw data into the database
        extraction.populatedb(db, incidents)

    # Augment the data
    augmented_data = augmentation.augment_data(db)

    # Redirect to csv file
    with open("../resources/normanpd_augmented.csv", "w") as f:
        # header = ["Day of the Week", "Time of Day", "Weather", "Location Rank", "Side of Town", "Incident Rank", "Nature", "EMSSTAT"]
        header = ["Date (YYYY-MM-DD)", "Day of the Week", "Time of Day", "Location", "Location Rank", "Incident Nature", "Incident Rank"]

        f.write("\t".join(header) + "\n")
        # Print the header to stdout
        # print("\t".join(header), file=sys.stdout)

        for row in augmented_data:
            f.write("\t".join(map(str, row)) + "\n")
            # Print each row to stdout
            # print("\t".join(map(str, row)), file=sys.stdout)

    # Close the database connection
    db.close()

    # Read the augmented data from the csv file
    augmented_df = pd.read_csv("../resources/normanpd_augmented.csv", sep="\t")
    st.write(augmented_df)

    return augmented_df

def main():
    # Create a form with a date picker in the sidebar
    with st.form(key ='Form1'):
        st.success("Select a date range below to visualise the incident summary data")
        selected_date_range = st.date_input("Select Date Range", 
                                            value=(st.session_state.incident_date_range[0], st.session_state.incident_date_range[1]), 
                                            min_value=min_date, max_value=max_date, format="MM/DD/YYYY")

        submit_button = st.form_submit_button("Download / View data for selected dates")

    if submit_button:
        # Save the selected range into a state variable
        if selected_date_range:
            st.session_state.incident_date_range = selected_date_range
            st.write("Selected date range: ", st.session_state.incident_date_range[0], " - ", st.session_state.incident_date_range[1])

        # Get all the dates in the selected range
        all_dates = pd.date_range(start=st.session_state.incident_date_range[0], end=st.session_state.incident_date_range[1], freq='D').to_list()

        # Download the incident data for each selected date
        download_pdfs(all_dates)



if __name__ == '__main__':
    # Call the main function
    main()
