# Norman Police Department Incident Visualization

Name: Bhagya Raj Varadaraju\
Email: bhagyaraj.varadaraju@gmail.com

# Project Description

In this project, we perform data extraction on the Norman Police Department incident summary pdf files by fetching them using URLs and then the extracted data is augmented. This program reads the pdf files and extracts the data using pypdf library for all the dates the user selects. It then parses the file and converts all the incident-related data into a list of lists. This data is then stored as a dataframe with the following columns:

- incident_time
- incident_number
- incident_location
- incident_nature
- incident_ori

This dataframe is then read and transformed to contain the following information:

- Date (YYYY-MM-DD)
- Day of the Week
- Time of Day
- Location
- Latitude
- Longitude
- Location Rank
- Incident Nature
- Incident Rank

This augmented data is then used to visualize and understand the trends in the incidents that occur in Norman, OK. The Norman Police Department can use this to manage the incidents that occur in Norman, OK, and take necessary actions to prevent them.

## Dependencies
- pypdf
- pytest
- setuptools
- geopy
- requests
- numpy
- pandas
- streamlit
- seaborn
- altair

# How to install
- curl https://pyenv.run | bash
- pyenv install 3.11
- pyenv global 3.11
- pip install pipenv --user
- pipenv install

## How to run / Video walkthrough
For running the program: **_streamlit run src/NormanPD.py_**

https://github.com/bhagyaraj-varadaraju/Norman-PD-Data-Visualization/assets/20358558/aa588a88-105e-4d63-a4e8-e42be3417e99

For running pytest: **_pipenv run python -m pytest_**

## Functions
### src/NormanPD.py
- main() - _This is the main function to get input dates from the user._
- extract_pdf_data(date) - _This function takes the date as input and extracts the data from the pdf file and returns a list of lists containing the incident data._
- transform_data(all_dates) - _This function takes the list of dates as input and transforms the data into a dataframe with the required columns._
- load_data(augmented_data) - _This function takes the augmented data as input and loads it into the app._

### src/utils/augmentation.py
- augment_data(incidents) - _This function takes the connection to the database as input and augments the data with the required information. It returns the augmented data as a list of lists._

### src/utils/augmentation_helper.py
- get_day_of_week(date) - _This function takes the date as input and returns the day of the week._
- get_time_of_day(time) - _This function takes the time as input and returns the time of the day._
- get_location_ranks(db) - _This function takes the database connection as input and returns a dictionary with the location as the key and the rank as the value._
- get_incident_ranks(db) - _This function takes the database connection as input and returns a dictionary with the incident nature as the key and the rank as the value._
- get_emsstat(incidents) - _This function takes the list of incidents as input and returns a dictionary with the row number as the key and the emsstat_value as the value._

### src/utils/extraction.py
- fetchincidents(date, url) - _This function fetches the pdf file from the given URL and returns the data in io.BytesIO format._
- extractincidents(date, data) - _This function takes the data in io.BytesIO format as input and extracts the data from the pdf file and returns a list of lists containing the incident data._

### src/utils/location_helper.py
- get_side_of_town(location) - _This function takes the location as input and returns the side of the town._
- get_lat_long(location) - _This function takes the location as input and returns the latitude and longitude of the location._
- is_lat_long(location) - _This function takes the location as input and returns True if the location is already in latitude and longitude format, else False._

### src/utils/weather_helper.py
- get_weather_code(time, location) - _This function takes the time and location as input and returns the weather code._
- get_date(incident_time) - _This function takes the incident time as input and returns the date in the format needed by open-meteo historical weather API._
- get_weather_data(lat, long, date) - _This function takes the latitude, longitude, and date as input and returns the weather data from the open-meteo historical weather API._

### src/pages/Incidents_Frequency.py
- plot_data() - _This plot illustrates the incident count by hour for the selected dates._

### src/pages/Critical_Incidents.py
- plot_data() - _This plot visualizes the top 10 incident natures by the frequency of their occurrence during the dates you selected. You can select additional incident natures to compare them against the top 10 incident types._

### src/pages/Crime_Hotspots.py
- plot_data() - _This graph illustrates the incident frequency by the location of the incident during the selected dates. You can select additional locations to compare them against the top 25 Hotspots._

## Bugs and Assumptions

The following assumptions are made:
- A valid row must contain more than 2 columns
- A row that has an empty nature column must contain 3 columns time, number, and ORI of the incident
- All pages must have the same 5 columns mentioned above in the same order
- The pdf that is being extracted must be a normanpd incident summary with the same header and footer as the sample pdf file in docs
- In the augmented data when the location is not converting to latitude and longitude, weather and side of town will be considered as an empty string
- The side of the town is determined by the incident location's position w.r.t. the center of Norman, OK. And the direction is determined by the angle between the incident location and the center of Norman, OK. This angle is calculated using the geographiclib library.
- Each direction consists of 45 degrees of angle around the center with zero starting at the geographic north.

##

## Testcase Discussion

- test_fetchincidents_valid_url() - _This is to check if the program can fetch the pdf file from the given URL._
- test_fetchincidents_invalid_url() - _This is to check if the program can raise an HTTP error if the URL is invalid._
- test_extractincidents() - _This is to check if the program can extract the data from a given sample pdf file._
- test_createdb_connection() - _This is to check if the program can create a database successfully._
- test_createdb_table_existence() - _This is to check if the program can create a table successfully._
- test_createdb_table_schema() - _This is to check if the table created by the program has the expected schema._
- test_populatedb() - _This is to check if the program can populate the database with the extracted data successfully._
- test_augment_data() - _This is to check if the program can augment the data with the required information successfully._
##
