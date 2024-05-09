import streamlit as st
import pandas as pd
import seaborn as sns
import argparse
import os, sys
from src import extraction, augmentation


st.set_page_config(layout="centered")
st.title('Incident Summaries in Norman, OK')

def main(urls_file):
    #Read the file and get the url from each line
    with open(urls_file, 'r') as f:
        urls = f.readlines()
        # Delete the old db file if it exists
        try:
            os.remove("resources/normanpd_raw.db")
            os.remove("resources/normanpd_augmented.csv")
        except FileNotFoundError:
            pass

        db = None
        # Iterate through each url and extract the raw incident data
        for url in urls:
            # Remove the newline character
            url = url.strip()

            # Download data
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
    with open("resources/normanpd_augmented.csv", "w") as f:
        # header = ["Date (YYYY-MM-DD)", "Day of the Week", "Time of Day", "Weather", "Location Rank", "Side of Town", "Incident Rank", "Nature", "EMSSTAT"]
        header = ["Date (YYYY-MM-DD)", "Day of the Week", "Time of Day", "Location Rank", "Incident Rank", "Nature", "EMSSTAT"]

        f.write("\t".join(header) + "\n")
        # Print the header to stdout
        # print("\t".join(header), file=sys.stdout)

        for row in augmented_data:
            f.write("\t".join(map(str, row)) + "\n")
            # Print each row to stdout
            # print("\t".join(map(str, row)), file=sys.stdout)

    # Close the database connection
    db.close()

    # Plot the augmented data
    augmented_df = pd.read_csv("resources/normanpd_augmented.csv", sep="\t")
    st.write(augmented_df)


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", type=str, required=True, help="Incident summary urls file.")

    args = parser.parse_args()
    if args.urls:
        main(args.urls)
