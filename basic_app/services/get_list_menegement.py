import os
import sys
import django
import requests
from requests.auth import HTTPBasicAuth
import json
from icecream import ic
from basic_app.services.gen_random import generate_random_number

# 🔹 Ensure the script runs inside the Django project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add project root to path

# 🔹 Set Django settings module correctly (Change 'your_project' to your actual project name)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")  # Change this to your project name

# 🔹 Initialize Django
django.setup()

# 🔹 Import Django settings
# from django.conf import settings
# USERNAME = settings.username
# PASSWORD = settings.password
# print("✅ Loaded from settings:", USERNAME, PASSWORD)  # Debug
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

def get_list_management(ip, reqcount, begin_time, end_time):
    url = (
        f"http://{ip}/webs/getWhitelist?"
        f"action=list&group=LIST&uflag=0&usex=2&uage=0-100&MjCardNo=0&"
        f"begintime={begin_time}:00&endtime={end_time}&"
        f"utype=3&sequence=0&beginno=11&reqcount={reqcount}&sessionid=0&RanId={generate_random_number()}"
    )

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

# Example usage
# data = get_list_management(
#     ip="192.168.15.20",
#     username=USERNAME,
#     password=PASSWORD,
#     sequence=0,
#     reqcount=10000000000,
#     RanId=1234567890,
#     begin_time="2023-01-01",
#     end_time="2025-01-29"
# )

# # Save JSON to a file
# if data:
#     with open("list_management.json", "w") as file:
#         json.dump(data, file, indent=4)
#     print("✅ Data saved in JSON format.")
