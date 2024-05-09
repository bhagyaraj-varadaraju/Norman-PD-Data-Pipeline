import sqlite3, os
from extraction import createdb, populatedb


# Test the connection to the database
def test_createdb_connection():
    # Delete the database file
    try:
        os.remove('resources/normanpd_raw_test.db')
    except FileNotFoundError:
        pass

    # Connect to the database
    con = createdb('normanpd_raw_test')

    # Verify that the connection is not None
    assert con is not None

    # Close the connection
    con.close()


# Test the existence of the incidents table
def test_createdb_table_existence():
    # Delete the database file
    try:
        os.remove('resources/normanpd_raw_test.db')
    except FileNotFoundError:
        pass

    # Connect to the database
    con = createdb('normanpd_raw_test')

    # Verify that the incidents table exists
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents'")
    result = cur.fetchone()
    assert result is not None

    # Close the connection
    con.close()


# Test the schema of the incidents table
def test_createdb_table_schema():
    # Delete the database file
    try:
        os.remove('resources/normanpd_raw_test.db')
    except FileNotFoundError:
        pass

    # Connect to the database
    con = createdb('normanpd_raw_test')

    # Verify the schema of the incidents table
    cur = con.cursor()
    cur.execute("PRAGMA table_info(incidents)")
    columns = cur.fetchall()
    
    # Extract column names from tuples
    column_names = [column[1] for column in columns]

    expected_column_names = ['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori']
    for expected_column_name in expected_column_names:
        assert expected_column_name in column_names

    # Close the connection
    con.close()


# Utility function to test populatedb and createdb
def db_helper():
    # Create an in-memory SQLite database for testing
    con = sqlite3.connect(':memory:')
    cur = con.cursor()

    # Create the incidents table
    cur.execute('''CREATE TABLE incidents (incident_time TEXT, incident_number TEXT, incident_location TEXT, nature TEXT, incident_ori TEXT)''')

    # Sample list of incidents to insert
    incidents = [
        ('2024-02-05 10:00:00', '20240001', 'Main St', 'Theft', 'ORI123'),
        ('2024-02-06 11:00:00', '20240002', 'Broadway', 'Assault', 'ORI456'),
        ('2024-02-07 12:00:00', '20240003', 'Park Ave', 'Robbery', 'ORI789'),
        ('2024-02-08 12:00:00', '20240004', 'First St', 'Theft', 'ORI987'),
        ('2024-02-09 12:00:00', '20240005', '', '', 'ORI654')
    ]

    return con, incidents


# Test the populatedb function
def test_populatedb():
    # Delete the database file
    try:
        os.remove('resources/normanpd_raw_test.db')
    except FileNotFoundError:
        pass

    # Connect to the database
    con, incidents = db_helper()

    # Insert data into the database
    populatedb(con, incidents)

    # Verify that the database contains the expected number of records
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM incidents")
    num_records = cur.fetchone()[0]
    assert num_records == len(incidents)

    # Verify that the database contains the expected data
    cur.execute("SELECT * FROM incidents")
    records = cur.fetchall()
    assert records == incidents
