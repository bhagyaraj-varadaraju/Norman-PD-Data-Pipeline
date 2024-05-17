import streamlit as st
import urllib.request
import pypdf
import io
import re
import sqlite3


# Fetch the PDF from the URL
def fetchincidents(url):
    url = (url)
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"                          

    # Fetch the PDF from the URL
    try:
        data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
        return io.BytesIO(data)

    # Handle any HTTP errors that occur
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.reason}")
        raise

    # Handle any other errors that occur
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


# Extract each incident that includes a incident_time, incident_number, incident_location, nature, and incident_ori
def extractincidents(data):
    try:
        # Extract the text in the form of bytes from the PDF
        reader = pypdf.PdfReader(data)

        num_pages = len(reader.pages)
        incidents = []

        for i in range(num_pages):
            # Extract the text in the same layout of each source PDF page
            page = reader.pages[i]
            text = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False, layout_mode_scale_weight=1.0)

            # Split the text into rows based on new line character
            rows = text.split("\n")

            # Iterate through each row
            for row in rows:
                # Remove the title and subtitle of the PDF file
                row = row.replace('NORMAN POLICE DEPARTMENT', '')
                row = row.replace('Daily Incident Summary (Public)', '')

                if row != "":
                    # Split the row into incident fields based on multiple spaces
                    incident_fields = re.split(r'\s{2,}', row)
                    if len(incident_fields) > 2:
                        # Extract the incident_time, incident_number, and incident_ori
                        incident_time = incident_fields[0]
                        incident_number = incident_fields[1]
                        incident_ori = incident_fields[-1]

                        # Split the remaining row into incident_location and incident_nature
                        incident_location, incident_nature = "", ""
                        if len(incident_fields) > 3:
                            incident_location = incident_fields[2]
                            incident_nature = incident_fields[3]

                        # Append the split row to the incidents list
                        split_row = [incident_time.strip(), incident_number.strip(), incident_location.strip(), incident_nature.strip(), incident_ori.strip()]
                        incidents.append(split_row)

        # Return the list of incidents by removing the header of the PDF
        incidents = list(incidents[1:])
        return incidents

    # Handle any errors that occur
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


# Create an SQLite database file named normanpd.db in the resources/ directory and create an incidents table
def createdb(db_name):
    try:
        # Connect to the database
        con = sqlite3.connect(f'../../resources/{db_name}.db')
        cur = con.cursor()

        # Create the incidents table
        cur.execute('''CREATE TABLE IF NOT EXISTS incidents (incident_time TEXT, incident_number TEXT, incident_location TEXT, nature TEXT, incident_ori TEXT)''')

        # Commit the changes
        con.commit()

        # Return the connection
        return con

    # Handle any errors that occur
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        raise


# Insert the incidents data into the created SQLite database
def populatedb(con, incidents):
    # Insert the incidents data into the database
    cur = con.cursor()
    for incident in incidents:
        if len(incident) == 5:
            cur.execute('''INSERT INTO incidents VALUES (?, ?, ?, ?, ?)''', incident)

    # Commit and Close the connection
    con.commit()
