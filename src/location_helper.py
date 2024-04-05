from geopy.distance import geodesic
from geographiclib.geodesic import Geodesic
from geopy.geocoders import Nominatim
import re

# The side of town is one of eight items {N, S, E, W, NW, NE, SW, SE}. Side of town is determined by approximate orientation of the center of town 35.220833, -97.443611
def get_side_of_town(incident_location):
    # Get the latitude and longitude of the incident location
    incident_lat, incident_long = get_lat_long(incident_location)
    if incident_lat is None or incident_long is None:
        return None

    # Determine the side of town based on the orientation of the incident_location relative to the center of town
    center_lat, center_long = 35.220833, -97.443611
    # orientation = geodesic((center_lat, center_long), (incident_lat, incident_long)).bearing
    orientation = Geodesic.WGS84.Inverse(center_lat, center_long, incident_lat, incident_long)['azi1']

    # Each orientation is 45 degrees wide
    if orientation < 22.5 or orientation >= 337.5:
        return "N"
    elif 22.5 <= orientation < 67.5:
        return "NE"
    elif 67.5 <= orientation < 112.5:
        return "E"
    elif 112.5 <= orientation < 157.5:
        return "SE"
    elif 157.5 <= orientation < 202.5:
        return "S"
    elif 202.5 <= orientation < 247.5:
        return "SW"
    elif 247.5 <= orientation < 292.5:
        return "W"
    elif 292.5 <= orientation < 337.5:
        return "NW"
    else:
        return "Cannot determine side of town - Center"


def get_lat_long(incident_location):
    # Use the geopy library to get the latitude and longitude of the incident location
    geolocator = Nominatim(user_agent="norman-crime")
    try:
        if (is_lat_long(incident_location)):
            return float(incident_location.split(";")[0]), float(incident_location.split(";")[1])
        else:
            location = geolocator.geocode(incident_location)
            if location is None:
                return None, None
            return location.latitude, location.longitude
    except:
        return None, None

def is_lat_long(incident_location):
    # Check if the location is in the format of latitude;longitude using regex
    return re.match(r"^\d+\.\d+;\d+\.\d+$", incident_location) is not None
