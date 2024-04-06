from datetime import datetime
import pandas as pd

# Day of week is a numeric value in the range 1-7. Where 1 corresponds to Sunday and 7 corresonds of Saturday.
def get_day(day):
    day_num = datetime.strptime(day, '%m/%d/%Y').weekday() # Monday is 0 and Sunday is 6
    return ((day_num + 2) % 7) or 7    # Sunday is 1 and Saturday is 7


# Time of data is a numeric code from 0 to 24 describing the hour of the incident.
def get_time(time):
    time_num = int(datetime.strptime(time, '%H:%M').strftime('%H'))
    return time_num


# Determine the rank of the location based on the frequency of incidents at that location.
def get_location_ranks(db):
    # Create a dictionary to store the rank of the location based on the frequency of incidents at that location.
    location_ranks = {}
    cur = db.cursor()
    cur.execute('''SELECT incident_location, COUNT(*) FROM incidents GROUP BY incident_location ORDER BY COUNT(*) DESC, incident_location ASC''')
    rows = cur.fetchall()
    assigned_rank = 1

    # Assign the rank to the location based on the frequency of incidents at that location.
    for i, row in enumerate(rows):
        # If the frequency of the incident is the same as the previous incident, assign the same rank.
        if i == 0:
            location_ranks[row[0]] = assigned_rank
        elif rows[i-1][1] == row[1]:
            location_ranks[row[0]] = assigned_rank
        # If the frequency of the incident is different from the previous incident, assign a new rank.
        else:
            location_ranks[row[0]] = i + 1
            assigned_rank = i + 1

    return location_ranks


# Determine the rank of the incident based on the frequency of the incident nature.
def get_incident_ranks(db):
    # Create a dictionary to store the rank of the incident based on the frequency of the incident nature.
    incident_ranks = {}
    cur = db.cursor()
    cur.execute('''SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY COUNT(*) DESC, nature ASC''')
    rows = cur.fetchall()
    assigned_rank = 1

    # Assign the rank to the incident based on the frequency of the incident_nature.
    for i, row in enumerate(rows):
        # If the frequency of the incident is the same as the previous incident, assign the same rank.
        if i == 0:
            incident_ranks[row[0]] = assigned_rank
        elif rows[i-1][1] == row[1]:
            incident_ranks[row[0]] = assigned_rank
        # If the frequency of the incident is different from the previous incident, assign a new rank.
        else:
            incident_ranks[row[0]] = i + 1
            assigned_rank = i + 1

    return incident_ranks


# EMSSTAT is a boolean value based on the incident_ori value.
def get_emsstat(incidents):
    # Case 1 - Return True if the incident_ori is EMSSTAT
    # Case 2 - Return True if the incident_ori for any subsequent record or two (any records) is EMSSTAT at the same time and location
    emsstat_values = {}

    # Make the incidents array a dataframe to make it easier to traverse through the records
    incidents_df = pd.DataFrame(incidents, columns=['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori'])

    # Replace all 'EMSSSTAT' values with 1 and all other values with 0
    incidents_df['emsstat'] = incidents_df['incident_ori'].apply(lambda x: 1 if x == 'EMSSTAT' else 0)

    # Now, replace all the values in the 'emsstat' column with 1 if the any record with same date and location has 'EMSSTAT' value which is now 1
    incidents_df['emsstat'] = incidents_df.groupby(['incident_time', 'incident_location'])['emsstat'].transform(lambda x: 1 if x.any() else 0)

    # Convert the 'emsstat' column to a dictionary
    emsstat_values = incidents_df['emsstat'].to_dict()

    return emsstat_values
