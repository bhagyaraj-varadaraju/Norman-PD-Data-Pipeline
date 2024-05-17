import os, io
from augmentation_utils import augment_data
from extraction import createdb, populatedb, extractincidents

def test_augment_data():
    # Delete the database file
    try:
        os.remove('resources/normanpd_raw_test.db')
    except FileNotFoundError:
        pass

    # Get the sample pdf data
    with open ("docs/2024-01-25_daily_incident_summary.pdf", "rb") as file:
        sample_pdf_data = file.read()

    # Call the extractincidents function
    incidents = extractincidents(io.BytesIO(sample_pdf_data))

    # Connect to the database
    con = createdb('normanpd_raw_test')

    # Populate the database
    populatedb(con, incidents)

    # Augment the data
    augmented_data = augment_data(con)

    # Verify that the augmented data is not empty
    assert augmented_data is not None

    # Verify that the augmented data contains the expected information
    expected_data = [[5, 0, 3, 4, 'SE', 4, 'Check Area', 0],
                     [5, 0, 3, 4, 'N', 1, 'Traffic Stop', 0],
                     [5, 0, 3, 4, 'N', 4, 'Alarm', 0],
                     [5, 0, 3, 1, 'NE', 2, 'Abdominal Pains/Problems', 1],
                     [5, 0, 3, 1, 'NE', 2, 'Abdominal Pains/Problems', 1],
                     [5, 0, 3, 4, 'N', 4, 'Larceny', 0],
                     [5, 0, 3, 4, 'N', 4, 'Suspicious', 0],
                     [5, 0, 3, 4, 'SE', 1, 'Traffic Stop', 0],
                     [5, 0, 3, 4, 'S', 4, 'Fire Alarm', 0],
                     [5, 0, '', 4, '', 1, 'Traffic Stop', 0],
                     [5, 0, 3, 1, 'SE', 2, 'Preg/Child Birth/Miscarriage', 1],
                     [5, 0, 3, 1, 'SE', 2, 'Preg/Child Birth/Miscarriage', 1],
                     [5, 0, '', 1, '', 1, 'Traffic Stop', 0],
                     [5, 0, '', 1, '', 4, 'Warrant Service', 0],
                     [5, 0, '', 4, '', 4, 'Noise Complaint', 0],
                     [5, 1, 3, 4, 'N', 1, 'Traffic Stop', 0]]

    # Verify that the augmented data is as expected
    assert expected_data == augmented_data

    # Close the connection
    con.close()
