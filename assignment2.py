import argparse
import os
from src import utils, augment

def main(urls_file):
    #Read the file and get the url from each line
    with open(urls_file, 'r') as f:
        urls = f.readlines()
        # Delete the old db file if it exists
        try:
            os.remove("resources/normanpd_raw.db")
        except FileNotFoundError:
            pass

        db = None
        # Iterate through each url and extract the raw incident data
        for url in urls:
            # Remove the newline character
            url = url.strip()

            # Download data
            incident_data = utils.fetchincidents(url)

            # Extract data
            incidents = utils.extractincidents(incident_data)

            # Create new database
            db = utils.createdb("normanpd_raw")

            # Insert the extracted raw data into the database
            utils.populatedb(db, incidents)

    # Augment the data
    augmented_data = augment.augment_data(db)

    # Redirect to csv file
    with open("resources/normanpd_augmented.csv", "w") as f:
        for row in augmented_data:
            f.write(",".join(map(str, row)) + "\n")

    # # Print to stdout
    # header = ["Day of the Week", "Time of Day", "Weather", "Location Rank", "Side of Town", "Incident Rank", "Nature", "EMSSTAT"]
    # print("\t".join(header))
    # for row in augmented_data:
    #     print("\t".join(map(str, row)))

    # Close the database connection
    db.close()


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", type=str, required=True, help="Incident summary urls file.")

    args = parser.parse_args()
    if args.urls:
        main(args.urls)
