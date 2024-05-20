import streamlit as st
import pandas as pd
import argparse
import os, datetime, sys
from utils import extraction, augmentation


# Set the page configuration
st.set_page_config(layout="wide", page_title="Norman Police Department App", page_icon="🚔")
st.title('Incident Summaries in Norman, OK')

# Assign a default value to the date picker state
today = datetime.datetime.now()
min_date = datetime.date(today.year, 12, 1) if (today.month == 1) else datetime.date(today.year, today.month - 1, 1)
max_date = datetime.date(today.year, today.month, today.day) if (today.day < 3) else datetime.date(today.year, today.month, today.day - 2)

if "incident_date_range" not in st.session_state:
    st.session_state.incident_date_range = [min_date, max_date]


# Download and augment the incident data for the selected dates
@st.cache_data
def download_data(all_dates):
    # Delete the old db file if it exists
    try:
        os.remove("./resources/normanpd_augmented.csv")
    except FileNotFoundError:
        pass

    incidents = []

    # Iterate through each url and extract the raw incident data
    for date in all_dates:
        # Create the url for each selected date
        ## Example URL: https://www.normanok.gov/sites/default/files/documents/YYYY-MM/YYYY-MM-DD_daily_incident_summary.pdf
        url = "https://www.normanok.gov/sites/default/files/documents/" + date.strftime("%Y-%m") + "/" + date.strftime("%Y-%m-%d") + "_daily_incident_summary.pdf"

        # Download data from the url
        incident_data = extraction.fetchincidents(url)

        # Extract data
        incidents.extend(extraction.extractincidents(incident_data))

    # Augment the data
    augmented_data = augmentation.augment_data(incidents)

    # Redirect to csv file
    with open("./resources/normanpd_augmented.csv", "w") as f:
        # header = ["Day of the Week", "Time of Day", "Weather", "Location Rank", "Side of Town", "Incident Rank", "Nature", "EMSSTAT"]
        header = ["Date (YYYY-MM-DD)", "Day of the Week", "Time of Day", "Location", "Location Rank", "Incident Nature", "Incident Rank"]
        f.write("\t".join(header) + "\n")

        for row in augmented_data:
            f.write("\t".join(map(str, row)) + "\n")


@st.cache_data
def view_data(all_dates, csv_file):
    if os.path.exists(csv_file):
        # Read the augmented data from the csv file
        augmented_df = pd.read_csv(csv_file, sep="\t")

        # Display the augmented data
        st.write(augmented_df)

def main():
    # Create a form with a date picker in the sidebar
    with st.form(key ='Form1'):
        st.success(f"Select a date range between {st.session_state.incident_date_range[0]} and {st.session_state.incident_date_range[1]} to download and view the incident data")
        selected_date_range = st.date_input(("Select a date range:"), 
                                            value=(st.session_state.incident_date_range[0], st.session_state.incident_date_range[1]), 
                                            min_value=min_date, max_value=max_date, format="MM/DD/YYYY")

        submit_button = st.form_submit_button("Download/View data for selected dates")

    all_dates = []
    if submit_button:
        # Save the selected range into a state variable
        st.session_state.incident_date_range = selected_date_range
        st.write("You Selected: ", st.session_state.incident_date_range[0], " - ", st.session_state.incident_date_range[1])

        # Get all the dates in the selected range
        all_dates = pd.date_range(start=st.session_state.incident_date_range[0], end=st.session_state.incident_date_range[1], freq='D').to_list()

        # Download the incident data for each selected date
        download_data(all_dates)

        # View the augmented data
        view_data(all_dates, "./resources/normanpd_augmented.csv")


if __name__ == '__main__':
    # Call the main function
    main()
