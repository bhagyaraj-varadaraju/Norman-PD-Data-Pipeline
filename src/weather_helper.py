import requests
from src import location_helper, augment_utils
from datetime import datetime


# Determine the weather at the time and location of the incident
def get_weather_code(incident_time, incident_location):
    # Get the latitude and longitude of the incident location
    incident_lat, incident_long = location_helper.get_lat_long(incident_location)
    if incident_lat is None or incident_long is None:
        return ''

    # Get the date of the incident
    date = get_date(incident_time)

    # Get the weather code at the time and location of the incident
    data = get_weather_data(incident_lat, incident_long, date)
    if data is None:
        return None

    # Return the weather code value by parsing the data
    return data.get('hourly').get('weather_code')[augment_utils.get_time(incident_time.split()[1])]


def get_date(incident_time):
    date = incident_time.split()[0]
    return datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')


def get_weather_data(lat, long, date):
    # Get the weather data from the weather API
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": long,
        "start_date": date,
        "end_date": date,
        "hourly": "weather_code",
        "timezone": "America/Chicago"
    }
    data = requests.get(url, params).json()
    return data
