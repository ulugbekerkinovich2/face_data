import requests
from requests.auth import HTTPBasicAuth
import json


def fetch_control_data(ip, 
                       username, 
                       password, 
                       ustatus, 
                       usex, 
                       uage, 
                       MjCardNo, 
                       begintime, 
                       endtime, 
                       utype, 
                       sequence, 
                       beginno, 
                       reqcount, 
                       sessionid, 
                       ranid, 
                       output_file="control_data.json"):
    url = (
        f"http://{ip}/webs/getControl?"
        f"action=list&group=CONTROL&ustatus={ustatus}&usex={usex}&uage={uage}&MjCardNo={MjCardNo}&"
        f"begintime={begintime}&endtime={endtime}&utype={utype}&sequence={sequence}&"
        f"beginno={beginno}&reqcount={reqcount}&sessionid={sessionid}&RanId={ranid}"
    )

    try:
        # Perform the GET request with Basic Authentication
        response = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=15)

        # Check if the request was successful
        response.raise_for_status()

        # Parse response text to JSON
        raw_data = response.text
        json_data = parse_raw_to_json(raw_data)

        # Save JSON data to a file
        with open(output_file, "w") as file:
            json.dump(json_data, file, indent=4)

        print(f"Capture logs data successfully saved as '{output_file}'.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def parse_raw_to_json(raw_data):
    """
    Converts raw server response to JSON format.

    :param raw_data: Raw string data from the server.
    :return: Parsed JSON object.
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
            current[keys[-1]] = value.strip()  # Remove extra spaces
    return json_data


# Example usage
fetch_control_data(
    ip="192.168.15.20",        # Server IP
    username="admin",          # Basic Auth username
    password="aifu1q2w3e4r@",  # Basic Auth password
    ustatus=0,                 # User status
    usex=2,                    # User sex
    uage="0-100",              # User age range
    MjCardNo=0,                # Card number
    begintime="2023-01-24/00:00:00",  # Start time
    endtime="2025-01-29/23:59:59",    # End time
    utype=0,                   # User type
    sequence=1,                # Sequence number
    beginno=0,                 # Begin number
    reqcount=10000000,         # Request count
    sessionid=264,             # Session ID
    ranid=72185954,            # Random ID
    output_file="control_data.json"   # Output file name
)