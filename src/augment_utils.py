from datetime import datetime


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
    location_rank = {}
    cur = db.cursor()
    cur.execute('''SELECT incident_location, COUNT(*) FROM incidents GROUP BY incident_location ORDER BY COUNT(*) DESC, incident_location ASC''')
    rows = cur.fetchall()
    assigned_rank = 1

    # Assign the rank to the location based on the frequency of incidents at that location.
    for i, row in enumerate(rows):
        # If the frequency of the incident is the same as the previous incident, assign the same rank.
        if i == 0:
            location_rank[row[0]] = assigned_rank
        elif rows[i-1][1] == row[1]:
            location_rank[row[0]] = assigned_rank
        # If the frequency of the incident is different from the previous incident, assign a new rank.
        else:
            location_rank[row[0]] = i + 1
            assigned_rank = i + 1

    return location_rank


# Determine the rank of the incident based on the frequency of the incident nature.
def get_incident_ranks(db):
    # Create a dictionary to store the rank of the incident based on the frequency of the incident nature.
    incident_rank = {}
    cur = db.cursor()
    cur.execute('''SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY COUNT(*) DESC, nature ASC''')
    rows = cur.fetchall()
    assigned_rank = 1

    # Assign the rank to the incident based on the frequency of the incident_nature.
    for i, row in enumerate(rows):
        # If the frequency of the incident is the same as the previous incident, assign the same rank.
        if i == 0:
            incident_rank[row[0]] = assigned_rank
        elif rows[i-1][1] == row[1]:
            incident_rank[row[0]] = assigned_rank
        # If the frequency of the incident is different from the previous incident, assign a new rank.
        else:
            incident_rank[row[0]] = i + 1
            assigned_rank = i + 1

    return incident_rank


# EMSSTAT is a boolean value based on the incident_ori value.
def get_emsstat(incident_row_num, incident_ori, incidents):
    # Return True if the incident_ori is EMSSTAT
    if incident_ori == "EMSSTAT":
        return 1
    
    # Return True if the subsequent record or two contain an EMSSTAT at the same time and location
    # Checking for EMSSTAT, till the records have same time and location
    for i in range(incident_row_num+1, len(incidents)):
        if incidents[i][0] == incidents[incident_row_num][0]:   # Check if the time is same
            if incidents[i][2] == incidents[incident_row_num][2]:   # Check if the location is same
                if incidents[i][4] == "EMSSTAT":    # Check if the incident_ori is EMSSTAT
                    return 1
        else:
            break

    # Return False otherwise
    return 0
