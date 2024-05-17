from geographiclib.geodesic import Geodesic
from geopy.geocoders import Nominatim
import re


# The side of town is one of eight items {N, S, E, W, NW, NE, SW, SE}. Side of town is determined by approximate orientation to the center of town (35.220833, -97.443611).
def get_side_of_town(incident_location):
    # Get the latitude and longitude of the incident location
    incident_lat, incident_long = get_lat_long(incident_location)
    if incident_lat is None or incident_long is None:
        return ''

    # Determine the side of town based on the orientation of the incident_location relative to the center of town
    center_lat, center_long = 35.220833, -97.443611
    orientation = Geodesic.WGS84.Inverse(center_lat, center_long, incident_lat, incident_long)['azi1']

    # Each orientation is 45 degrees wide
    if orientation < 0:
        orientation += 360

    sector = int((orientation + 22.5) / 45) % 8
    sides_of_town = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    return sides_of_town[sector]


# Get the latitude and longitude of the incident location
def get_lat_long(incident_location):
    try:
        # Return the latitude and longitude if the location is in the format of latitude;longitude
        if (is_lat_long(incident_location)):
            return float(incident_location.split(";")[0]), float(incident_location.split(";")[1])
        else:
            # Append the city name to the location and get the latitude and longitude
            location = Nominatim(user_agent="normanpd-dataset").geocode(f"{incident_location}, NORMAN, OK")
            if location is None:
                return None, None
            return location.latitude, location.longitude
    except Exception:
        return None, None


# Check if the location is in the format of latitude;longitude using regex
def is_lat_long(incident_location):
    return re.match(r"^-?\d+\.\d+;-?\d+\.\d+$", incident_location) is not None
