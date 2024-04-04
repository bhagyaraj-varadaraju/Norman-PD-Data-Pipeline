import argparse
from src import utils, augment

def main(urls_file):
    #Read the file and get the url from each line
    with open(urls_file, 'r') as f:
        urls = f.readlines()
        for i, url in zip(range(len(urls)), urls):
            # Remove the newline character
            url = url.strip()

            # Download data
            incident_data = utils.fetchincidents(url)

            # Extract data
            incidents = utils.extractincidents(incident_data)

            # Create new database
            db = utils.createdb()

            # Insert data
            utils.populatedb(db, incidents)

            # Print the progress by showing the number of urls processed till now
            print(f"Processed number:{i+1} url")


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", type=str, required=True, help="Incident summary urls file.")

    args = parser.parse_args()
    if args.urls:
        main(args.urls)
