from utils import augmentation_helper, weather_helper, location_helper
from sqlalchemy import text
import pandas as pd


# Read and augment the data from the database
def augment_data(incidents):
    # Raw incident structure: [incident_time, incident_number, incident_location, incident_nature, incident_ori]
    # Augmented data row: [Date of the Incident, Day of the Week, Time of Day, Weather, Location Rank, Side of Town, Incident Rank, Nature, EMSSTAT]
    augmented_data = []

    # Create a dataframe to store the incidents
    incidents_df = pd.DataFrame(incidents, columns=['incident_time', 'incident_number', 'incident_location', 'incident_nature', 'incident_ori'])

    # Create and populate the location_ranks dictionary
    location_ranks = augmentation_helper.get_location_ranks(incidents_df)

    # Create and populate the incident_ranks dictionary
    incident_ranks = augmentation_helper.get_incident_ranks(incidents_df)

    # Create and populate the emsstat dictionary
    emsstat_values = augmentation_helper.get_emsstat(incidents_df)

    # Augment the data
    for row_num, incident in enumerate(incidents):
        output_row = []

        # Get the date of the incident
        output_row.append(augmentation_helper.get_date(incident[0]))

        # Get the day of the week the incident occurred
        output_row.append(augmentation_helper.get_day(incident[0].split()[0]))

        # Get the time of day the incident occurred
        output_row.append(augmentation_helper.get_time(incident[0].split()[1]))

        # Get the weather at the time and location of the incident
        # output_row.append(weather_helper.get_weather_code(incident[0], incident[2]))

        # Get the location of the incident
        output_row.append(incident[2])

        # Get the latitude and longitude of the incident location
        # output_row.append(location_helper.get_lat_long(incident[2]))

        # Get the incident_location rank
        output_row.append(location_ranks[incident[2]])

        # Get the side of town using the incident_location
        # output_row.append(location_helper.get_side_of_town(incident[2]))

        # Get the nature of the incident
        output_row.append(incident[3])

        # Get the incident_nature rank
        output_row.append(incident_ranks[incident[3]])

        # Get the EMSSTAT value
        # output_row.append(emsstat_values[row_num])

        # Append the augmented data row to the list
        augmented_data.append(output_row)

    return augmented_data
