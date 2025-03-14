import requests
from basic_app.services.upload_image import upload_image
from basic_app.services.gen_random import generate_random_number
from icecream import ic
from requests.auth import HTTPBasicAuth
import re
USERNAME = "admin"
PASSWORD = "aifu1q2w3e4r@"
def parse_raw_to_json(raw_data):
    """
    Parses raw data into JSON.
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
def delete_user(ip, uid, RanId ):
    url = f"http://{ip}/webs/setWhitelist?action=del&group=LIST&LIST.uid={uid}&nRanId={RanId}"
    try:
        # Perform GET request with Basic Authentication
        response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()  # Check response status

        # Parse response
        raw_data = response.text
        json_data = parse_raw_to_json(raw_data)
        root = json_data.get("root", {})
        list_data = root.get("LIST", {})

        # ITEMXX nomli kalitlarni ajratib olish
        face_data_list = [
            value for key, value in list_data.items() if key.startswith("ITEM")
        ]
        return face_data_list
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request error occurred: {req_err}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None