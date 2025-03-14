# import requests
# from requests.auth import HTTPBasicAuth
# import json


# def fetch_control_data(ip,
#                        username,
#                        password,
#                        ustatus,
#                        usex,
#                        uage,
#                        MjCardNo,
#                        begintime,
#                        endtime,
#                        utype,
#                        sequence,
#                        beginno,
#                        reqcount,
#                        sessionid,
#                        ranid,
#                        output_file="control_data.json"):
#     url = (
#         f"http://{ip}/webs/getControl?"
#         f"action=list&group=CONTROL&ustatus={ustatus}&usex={usex}&uage={uage}&MjCardNo={MjCardNo}&"
#         f"begintime={begintime}&endtime={endtime}&utype={utype}&sequence={sequence}&"
#         f"beginno={beginno}&reqcount={reqcount}&sessionid={sessionid}&RanId={ranid}"
#     )

#     try:
#         # Perform the GET request with Basic Authentication
#         response = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=60)

#         # Check if the request was successful
#         response.raise_for_status()

#         # Parse response text to JSON
#         raw_data = response.text
#         json_data = parse_raw_to_json(raw_data)

#         # Save JSON data to a file
#         with open(output_file, "w") as file:
#             json.dump(json_data, file, indent=4)

#         print(f"Capture logs data successfully saved as '{output_file}'.")

#     except requests.exceptions.HTTPError as http_err:
#         print(f"HTTP error occurred: {http_err}")
#     except requests.exceptions.RequestException as req_err:
#         print(f"Request error occurred: {req_err}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")


# def parse_raw_to_json(raw_data):
#     """
#     Converts raw server response to JSON format.

#     :param raw_data: Raw string data from the server.
#     :return: Parsed JSON object.
#     """
#     json_data = {}
#     for line in raw_data.splitlines():
#         line = line.strip()
#         if "=" in line:
#             key, value = line.split("=", 1)
#             keys = key.split(".")
#             current = json_data
#             for k in keys[:-1]:
#                 if k not in current:
#                     current[k] = {}
#                 current = current[k]
#             current[keys[-1]] = value.strip()  # Remove extra spaces
#     return json_data


# # Example usage
# fetch_control_data(
#     ip="192.168.15.20",        # Server IP
#     username="admin",          # Basic Auth username
#     password="aifu1q2w3e4r@",  # Basic Auth password
#     ustatus=0,                 # User status
#     usex=2,                    # User sex
#     uage="0-100",              # User age range
#     MjCardNo=0,                # Card number
#     begintime="2023-01-24/00:00:00",  # Start time
#     endtime="2025-01-29/23:59:59",    # End time
#     utype=0,                   # User type
#     sequence=1,                # Sequence number
#     beginno=0,                 # Begin number
#     reqcount=10000000,         # Request count
#     sessionid=264,             # Session ID
#     ranid=72185954,            # Random ID
#     output_file="control_data.json"   # Output file name
# )

# import requests
# from requests.auth import HTTPBasicAuth
# import json
# import time

# def fetch_control_data(
#     ip, username, password,
#     ustatus, usex, uage, MjCardNo,
#     begintime, endtime, utype, sequence,
#     beginno, reqcount, sessionid, ranid,
#     output_file="control_data.json", max_retries=3, retry_delay=5
# ):
#     url = (
#         f"http://{ip}/webs/getControl?"
#         f"action=list&group=CONTROL&ustatus={ustatus}&usex={usex}&uage={uage}&MjCardNo={MjCardNo}&"
#         f"begintime={begintime}&endtime={endtime}&utype={utype}&sequence={sequence}&"
#         f"beginno={beginno}&reqcount={reqcount}&sessionid={sessionid}&RanId={ranid}"
#     )

#     for attempt in range(max_retries):
#         try:
#             response = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=30)
#             response.raise_for_status()
#             raw_data = response.text

#             # Parse response
#             json_data = parse_raw_to_json(raw_data)

#             # ✅ Check for login timeout error
#             if json_data.get("root", {}).get("ERR", {}).get("des") == "loginTimeout":
#                 print(f"⚠️ Login timeout detected. Retry {attempt + 1}/{max_retries}")
#                 time.sleep(retry_delay)
#                 continue

#             # ✅ Save successful response to file
#             with open(output_file, "w") as file:
#                 json.dump(json_data, file, indent=4)

#             print(f"✅ Control data successfully saved to '{output_file}'")
#             return  # Success, so exit

#         except requests.exceptions.RequestException as e:
#             print(f"❌ Request error: {e}. Retry {attempt + 1}/{max_retries}")
#             time.sleep(retry_delay)

#     print(f"❌ Failed to fetch control data from {ip} after {max_retries} retries.")

# # Helper to convert raw response to structured JSON
# def parse_raw_to_json(raw_data):
#     json_data = {}
#     for line in raw_data.splitlines():
#         line = line.strip()
#         if "=" in line:
#             key, value = line.split("=", 1)
#             keys = key.split(".")
#             current = json_data
#             for k in keys[:-1]:
#                 current = current.setdefault(k, {})
#             current[keys[-1]] = value.strip()
#     return json_data



import os
import requests
from requests.auth import HTTPBasicAuth
import json
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def parse_raw_to_json(raw_data):
    json_data = {}
    for line in raw_data.splitlines():
        line = line.strip()
        if "=" in line:
            key, value = line.split("=", 1)
            keys = key.strip().split(".")
            current = json_data
            for k in keys[:-1]:
                current = current.setdefault(k, {})
            current[keys[-1]] = value.strip()
    return json_data

def fetch_control_data(
    ip, username, password,
    ustatus, usex, uage, MjCardNo,
    begintime, endtime, utype, sequence,
    beginno, reqcount, sessionid, ranid,
    max_retries=3, retry_delay=5
):
    url = (
        f"http://{ip}/webs/getControl?"
        f"action=list&group=CONTROL&ustatus={ustatus}&usex={usex}&uage={uage}&MjCardNo={MjCardNo}&"
        f"begintime={begintime}&endtime={endtime}&utype={utype}&sequence={sequence}&"
        f"beginno={beginno}&reqcount={reqcount}&sessionid={sessionid}&RanId={ranid}"
    )

    for attempt in range(max_retries):
        try:
            logger.info(f"🌐 Fetching control data (beginno: {beginno}) from {ip}")
            response = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=30)
            response.raise_for_status()
            json_data = parse_raw_to_json(response.text)

            if json_data.get("root", {}).get("ERR", {}).get("des") == "loginTimeout":
                logger.warning(f"⚠️ Login timeout on page {beginno}. Retrying...")
                time.sleep(retry_delay)
                continue

            return json_data

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request error: {e}")
            time.sleep(retry_delay)

    logger.error(f"❌ Failed to fetch control data from {ip} after {max_retries} retries.")
    return None

def fetch_all_control_data(
    ip, username, password,
    ustatus, usex, uage, MjCardNo,
    begintime, endtime, utype, sequence,
    sessionid, ranid,
    output_file="control_data_full.json",
    reqcount=5000
):
    all_logs = {}
    page = 0
    total_received = 0

    while True:
        beginno = page * reqcount
        logger.info(f"📄 Fetching page {page + 1} (beginno={beginno})")

        result = fetch_control_data(
            ip=ip,
            username=username,
            password=password,
            ustatus=ustatus,
            usex=usex,
            uage=uage,
            MjCardNo=MjCardNo,
            begintime=begintime,
            endtime=endtime,
            utype=utype,
            sequence=sequence,
            beginno=beginno,
            reqcount=reqcount,
            sessionid=sessionid,
            ranid=ranid
        )

        if not result:
            logger.info("❌ No data received or request failed. Stopping.")
            break

        page_logs = result.get("root", {}).get("CONTROL", {})
        received_count = sum(1 for key in page_logs if key.startswith("ITEM"))

        if not page_logs or received_count == 0:
            logger.info("✅ All data fetched. No more pages.")
            break

        all_logs.update(page_logs)
        total_received += received_count
        logger.info(f"✅ Page {page + 1} fetched. Received: {received_count}, Total so far: {total_received}")

        if received_count < reqcount:
            break

        page += 1

    final_data = {"root": {"CONTROL": all_logs}}
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(final_data, f, indent=4)

    logger.info(f"✅ All control data saved to '{output_file}' — {len(all_logs)} records total.")
