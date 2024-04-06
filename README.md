# cis6930sp24 -- Assignment2

Name: Bhagya Raj Varadaraju\
UFID: 6021-2561\
Email: varadaraju.b@ufl.edu

# Assignment Description (in your own words)

In this project, we perform data extraction on the Norman Police Department incident summary pdf files by fetching them using URLs and then the extracted data is augmented. This program reads the pdf files and extracts the data using pypdf library. It then parses the file and converts all the incident related data into a list of lists. This data is then stored in a SQLite database with a table called 'incidents'. It has the following columns:

- incident_time
- incident_number
- incident_location
- nature
- incident_ori

This table is then populated with all the extracted incident records. Then this db is read and augmented with the following information:

- Day of the Week
- Time of Day
- Weather
- Location Rank
- Side of Town
- Incident Rank
- Nature
- EMSSTAT

This augmented data is then stored in a csv file called 'augmented_data.csv'. It also prints the augmented data to stdout.

## Dependencies
- pypdf
- pytest
- setuptools
- geopy
- requests
- numpy
- pandas


# How to install
- curl https://pyenv.run | bash
- pyenv install 3.11
- pyenv global 3.11
- pip install pipenv --user
- pipenv install

## How to run / Video walkthrough
For running the program: **_pipenv run python assignment2.py --urls files.csv_**

https://github.com/bhagyaraj-varadaraju/cis6930sp24-assignment2/assets/20358558/29f34e0a-adef-4677-beb3-6b2eef2d8862

For running pytest: **_pipenv run python -m pytest_**

## Functions
### assignment2.py
- main(url_file) - _This is the main function   _

### augment_data.py
- augment_data(con) - _This function takes the connection to the database as input and augments the data with the required information. It returns the augmented data as a list of lists._

### augment_utils.py
- get_day_of_week(date) - _This function takes the date as input and returns the day of the week._
- get_time_of_day(time) - _This function takes the time as input and returns the time of the day._
- get_location_ranks(db) - _This function takes the database connection as input and returns a dictionary with the location as the key and the rank as the value._
- get_incident_ranks(db) - _This function takes the database connection as input and returns a dictionary with the incident nature as the key and the rank as the value._
- get_emsstat(incidents) - _This function takes the list of incidents as input and returns a dictionary with the row number as the key and the emsstat_value as the value._

### extract_utils.py
- fetchincidents(url) - _This function fetches the pdf file from the given url and returns the data in io.BytesIO format._
- extractincidents(data) - _This function takes the data in io.BytesIO format as input and extracts the data from the pdf file and returns a list of lists containing the incident data._
- createdb() - This function creates a sqlite database and the incidents table if it does not exist. It returns the database connection._
- populatedb(con, incidents) - _This function takes the connection to the database and the list of incidents as input and populates the database with the extracted data. It does not return anything._

### location_helper.py
- get_side_of_town(location) - _This function takes the location as input and returns the side of the town._
- get_lat_long(location) - _This function takes the location as input and returns the latitude and longitude of the location._
- is_lat_long(location) - _This function takes the location as input and returns True if the location is already in latitude and longitude format, else False._

### weather_helper.py
- get_weather_code(time, location) - _This function takes the time and location as input and returns the weather code._
- get_date(incident_time) - _This function takes the incident time as input and returns the date in the format needed by open-meteo historical weather api._
- get_weather_data(lat, long, date) - _This function takes the latitude, longitude and date as input and returns the weather data from the open-meteo historical weather api._


## Bugs and Assumptions

The following assumptions are made:
- A valid row must contain more than 2 columns
- A row that has an empty nature column must contain 3 columns time, number and ori of the incident
- All pages must have the same 5 columns mentioned above in the same order
- The pdf that is being extracted must be a normanpd incident summary with the same header and footer as the sample pdf file in docs
- In the augmented data when the location is not converting to latitude and longitude, weather and side of town will be considered as an empty string
- The side of the town is determined by the incident location's position wrt the center of Norman, OK. And the direction is determined by the angle between the incident location and the center of Norman, OK. This angle is calculated using the geographiclib library.
- Each direction consists of 45 degrees of angle around the center with zero starting at the geographic north.

If the input pdf file is not in compliance with these assumptions, then bugs of the same nature may occur.
##

## Testcase Discussion

- test_fetchincidents_valid_url() - _This is to check if the program is able to fetch the pdf file from the given url._
- test_fetchincidents_invalid_url() - _This is to check if the program is able to raise a HTTP error if the url is invalid._
- test_extractincidents() - _This is to check if the program is able to extract the data from a given sample pdf file._
- test_createdb_connection() - _This is to check if the program is able to create a database successfully._
- test_createdb_table_existence() - _This is to check if the program is able to create a table successfully._
- test_createdb_table_schema() - _This is to check if the table created by the program has the expected schema._
- test_populatedb() - _This is to check if the program is able to populate the database with the extracted data successfully._
- test_augment_data() - _This is to check if the program is able to augment the data with the required information successfully._
##
