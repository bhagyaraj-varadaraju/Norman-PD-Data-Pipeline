import pytest
import io
import urllib.request
from src.utils.extraction import fetchincidents, extractincidents

# Test urls
VALID_TEST_URL = "https://www.normanok.gov/sites/default/files/documents/2024-02/2024-02-01_daily_incident_summary.pdf"
INVALID_TEST_URL = "https://www.normanok.gov/sites/default/files/downloads/2024-02/2024-02-01_daily_incident_summary.pdf"


# Test the fetchincidents(url) function with a valid url
def test_fetchincidents_valid_url():
    test_url = VALID_TEST_URL
    result = fetchincidents(test_url)

    # Ensure the result is not none and is of type io.BytesIO
    assert result is not None
    assert isinstance(result, io.BytesIO)


# Test the fetchincidents(url) function with an invalid url
def test_fetchincidents_invalid_url():
    test_url = INVALID_TEST_URL
    
    # Use pytest.raises to check for an HTTPError
    with pytest.raises(urllib.error.HTTPError) as e:
        fetchincidents(test_url)
    
    # Ensure that it's a 404 error - Resource Not found
    assert e.value.code == 404
    assert e.value.reason == "Not Found"


# Test the extractincidents(data) function with the sample PDF data
def test_extractincidents():
    # Get the sample pdf data
    with open ("../docs/2024-01-25_daily_incident_summary.pdf", "rb") as file:
        sample_pdf_data = file.read()

    # Call the extractincidents function
    incidents = extractincidents(io.BytesIO(sample_pdf_data))

    # Check that the first row of incidents does not contain header information
    first_row = incidents[0]
    assert "NORMAN POLICE DEPARTMENT" not in first_row
    assert "Daily Incident Summary (Public)" not in first_row

    # Verify that the incidents list contains the expected data
    expected_incidents = [
        ['1/25/2024 0:00', '2024-00005499', '1446 TELLURIDE LN', 'Check Area', 'OK0140200'],
        ['1/25/2024 0:01', '2024-00005500', '2338 W LINDSEY ST', 'Traffic Stop', 'OK0140200'],
        ['1/25/2024 0:11', '2024-00005501', '3450 CHAUTAUQUA AVE', 'Alarm', 'OK0140200'],
        ['1/25/2024 0:18', '2024-00001408', '1916 DELANCEY DR', 'Abdominal Pains/Problems', '14005'],
        ['1/25/2024 0:18', '2024-00001749', '1916 DELANCEY DR', 'Abdominal Pains/Problems', 'EMSSTAT'],
        ['1/25/2024 0:20', '2024-00005502', '2550 MOUNT WILLIAMS DR', 'Larceny', 'OK0140200'],
        ['1/25/2024 0:28', '2024-00005503', '1325 W LINDSEY ST', 'Suspicious', 'OK0140200'],
        ['1/25/2024 0:33', '2024-00005504', '1197 12TH AVE SE', 'Traffic Stop', 'OK0140200'],
        ['1/25/2024 0:38', '2024-00001409', '103 W TIMBERDELL RD', 'Fire Alarm', '14005'],
        ['1/25/2024 0:46', '2024-00005505', 'GEORGE AVE / E LINDSEY ST', 'Traffic Stop', 'OK0140200'],
        ['1/25/2024 0:47', '2024-00001410', '1241 OAKHURST AVE', 'Preg/Child Birth/Miscarriage', '14005'],
        ['1/25/2024 0:47', '2024-00001750', '1241 OAKHURST AVE', 'Preg/Child Birth/Miscarriage', 'EMSSTAT'],
        ['1/25/2024 0:53', '2024-00005506', 'W LINDSEY ST / ED NOBLE PKWY', 'Traffic Stop', 'OK0140200'],
        ['1/25/2024 0:53', '2024-00005509', 'W LINDSEY ST / ED NOBLE PKWY', 'Warrant Service', 'OK0140200'],
        ['1/25/2024 0:53', '2024-00005507', 'DONNA DR / LOIS ST', 'Noise Complaint', 'OK0140200'],
        ['1/25/2024 1:05', '2024-00005508', '1006 N PORTER AVE', 'Traffic Stop', 'OK0140200']
    ]
    assert incidents == expected_incidents
