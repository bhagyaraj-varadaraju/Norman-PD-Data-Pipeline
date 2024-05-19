import requests
from utils import augmentation_helper, location_helper


# Determine the weather at the time and location of the incident
def get_weather_code(incident_time, incident_location):
    # Get the latitude and longitude of the incident location
    incident_lat, incident_long = location_helper.get_lat_long(incident_location)
    if incident_lat is None or incident_long is None:
        return ''

    # Get the date of the incident
    date = augmentation_helper.get_date(incident_time)

    # Get the weather code at the time and location of the incident
    data = get_weather_data(incident_lat, incident_long, date)
    if data is None:
        return None

    # Return the weather code value by parsing the data
    weather_code = data.get('hourly').get('weather_code')[augmentation_helper.get_time(incident_time.split()[1])]
    return weather_code if weather_code is not None else ''


# Get the weather response data from the weather API
def get_weather_data(lat, long, date):
    # Get the weather data from the weather API
    try:
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": long,
            "start_date": date,
            "end_date": date,
            "hourly": "weather_code",
            "timezone": "America/Chicago"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # Handle any HTTP errors that occur
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e.response.status_code} - {e.response.reason}")
        raise
