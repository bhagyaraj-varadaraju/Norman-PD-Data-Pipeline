from geopy.distance import geodesic
from datetime import datetime
from src import weather_helper, location_helper


# Read and augment the data from the database
def augment_data(db):
    # Each raw incident structure: [incident_time, incident_number, incident_location, incident_nature, incident_ori]
    # Each augmented data row: [Day of the Week, Time of Day, Weather, Location Rank, Side of Town, Incident Rank, Nature, EMSSTAT]
    augmented_data = []
    incidents = db.execute("SELECT * FROM incidents").fetchall()

    # Create and populate the location_rank dictionary
    location_rank = calculate_location_rank(db)

    # Create and populate the incident_rank dictionary
    incident_rank = calculate_incident_rank(db)

    # Augment the data
    for incident in incidents:
        output_row = []

        # Determine the day of week
        output_row.append(convert_day(incident[0].split()[0]))

        # Determine the time of day
        output_row.append(convert_time(incident[0].split()[1]))

        # Determine the weather at the time and location of the incident
        output_row.append(get_weather(incident[0], incident[2]))

        # Determine the location rank
        output_row.append(location_rank[incident[2]])

        # Determine the side of town
        output_row.append(determine_side(incident[2]))

        # Determine the incident rank
        output_row.append(incident_rank[incident[3]])

        # Append the nature of the incident
        output_row.append(incident[3])

        # Determine EMSSTAT
        output_row.append(get_emsstat(incident, incidents))

        # Append the augmented data row to the list
        augmented_data.append(output_row)

    return augmented_data


# Day of week is a numeric value in the range 1-7. Where 1 corresponds to Sunday and 7 corresonds of Saturday.
def convert_day(day):
    day_num = datetime.strptime(day, '%m/%d/%Y').weekday() # Monday is 0 and Sunday is 6
    return (day_num + 2) % 7    # Sunday is 1 and Saturday is 7


# Time of data is a numeric code from 0 to 24 describing the hour of the incident.
def convert_time(time):
    time_num = datetime.strptime(time, '%H:%M').hour
    return time_num


# Determine the weather at the time and location of the incident
def get_weather(time, location):
    #weather_code = weather_helper.determine_weather(time, location)
    return 1


# Determine the rank of the location based on the frequency of incidents at that location.
def calculate_location_rank(db):
    location_rank = {}
    cur = db.cursor()
    cur.execute('''SELECT incident_location, COUNT(*) FROM incidents GROUP BY incident_location ORDER BY COUNT(*) DESC, incident_location ASC''')
    rows = cur.fetchall()
    assigned_rank = 1

    for i, row in enumerate(rows):
        if i == 0:
            location_rank[row[0]] = assigned_rank
        elif rows[i-1][1] == row[1]:
            location_rank[row[0]] = assigned_rank
        else:
            location_rank[row[0]] = i + 1
            assigned_rank = i + 1

    return location_rank


# The side of town is one of eight items {N, S, E, W, NW, NE, SW, SE}. Side of town is determined by approximate orientation of the center of town 35.220833, -97.443611. You can use the geopy library for assistance.
def determine_side(location):
    # Your code here
    return "North"


# Determine the rank of the incident based on the frequency of the incident nature.
def calculate_incident_rank(db):
    incident_rank = {}
    cur = db.cursor()
    cur.execute('''SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY COUNT(*) DESC, nature ASC''')
    rows = cur.fetchall()
    assigned_rank = 1

    for i, row in enumerate(rows):
        if i == 0:
            incident_rank[row[0]] = assigned_rank
        elif rows[i-1][1] == row[1]:
            incident_rank[row[0]] = assigned_rank
        else:
            incident_rank[row[0]] = i + 1
            assigned_rank = i + 1

    return incident_rank


# This is a boolean value that is True in two cases. First, if the Incident ORI was EMSSTAT or if the subsequent record or two contain an EMSSTAT at the same time and locaton.
def get_emsstat(incident, incidents):
    # Your code here
    return "EMSSTAT"
