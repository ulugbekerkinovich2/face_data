import requests
from requests.auth import HTTPBasicAuth
import json


def fetch_capture_data(ip, username, password, begintime, endtime, utype, sequence, beginno, reqcount, sessionid, ranid, output_file="capture_data.json"):
    """
    Fetches capture data from the given IP using Basic Authentication and saves it in JSON format.

    :param ip: IP address of the server.
    :param username: Username for Basic Authentication.
    :param password: Password for Basic Authentication.
    :param begintime: Start time for data capture (format: "YYYY-MM-DD/HH:MM:SS").
    :param endtime: End time for data capture (format: "YYYY-MM-DD/HH:MM:SS").
    :param utype: User type parameter for the URL.
    :param sequence: Sequence parameter for the URL.
    :param beginno: Begin number parameter for the URL.
    :param reqcount: Request count parameter for the URL.
    :param sessionid: Session ID parameter for the URL.
    :param ranid: Random ID parameter for the URL.
    :param output_file: Name of the file to save the captured data to in JSON format.
    """
    url = (
        f"http://{ip}/webs/getCapture?"
        f"action=list&group=CAPTURE&begintime={begintime}&endtime={endtime}&"
        f"utype={utype}&sequence={sequence}&beginno={beginno}&reqcount={reqcount}&"
        f"sessionid={sessionid}&RanId={ranid}"
    )

    try:
        # Perform the GET request with Basic Authentication
        response = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=15)

        # Check if the request was successful
        response.raise_for_status()

        # Parse response text to JSON-compatible format
        raw_data = response.text
        json_data = parse_raw_to_json(raw_data)

        # Save JSON data to a file
        with open(output_file, "w") as file:
            json.dump(json_data, file, indent=4)
        print(f"Data successfully saved in JSON format to '{output_file}'.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def parse_raw_to_json(raw_data):
    """
    Parses raw text data into a JSON-compatible dictionary.

    :param raw_data: The raw text response from the server.
    :return: A dictionary containing parsed JSON data.
    """
    json_data = {}
    for line in raw_data.splitlines():
        line = line.strip()
        if "=" in line:
            key, value = line.split("=", 1)
            keys = key.split(".")
            current = json_data
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            current[keys[-1]] = value.strip()
    return json_data


# Example usage
fetch_capture_data(
    ip="192.168.15.20",        # Server IP
    username="admin",          # Basic Auth username
    password="aifu1q2w3e4r@",  # Basic Auth password
    begintime="2023-12-25/00:00:00",  # Start time
    endtime="2025-01-29/23:59:59",    # End time
    utype=0,                   # User type
    sequence=1,                # Sequence number
    beginno=0,                 # Begin number
    reqcount=100000000,        # Request count
    sessionid=0,               # Session ID
    ranid=66045881,            # Random ID
    output_file="stranger_capture_logs.json"   # Output file name
)