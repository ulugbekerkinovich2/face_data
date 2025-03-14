import requests
from basic_app.services.upload_image import upload_image
from basic_app.services.gen_random import generate_random_number
from icecream import ic
from requests.auth import HTTPBasicAuth
import re


def parse_response_to_json(html_data):
    """
    Parses the HTML response and converts it into a JSON object.
    """
    try:
        matches = re.findall(r'root\.(\w+)\s*=\s*([^\r\n]*)', html_data)
        result_json = {key: value.strip() for key, value in matches}
        return result_json
    except Exception as e:
        return {"error": f"Failed to parse response: {e}"}
    
def add_user(ip, username, password, dwfiletype=0, dwfileindex=1, dwfilepos=0, name="", text="", rfID_card=1, nRanId=0, gender=0):
    """
    Sends a POST request to add a user with the specified parameters and basic authentication.
    """
    url = f"http://{ip}/webs/setWhitelist"
    params = {
        "action": "add",
        "group": "LIST",
        "LIST.uid": "-1",
        "LIST.dwfiletype": dwfiletype,
        "LIST.dwfileindex": dwfileindex,
        "LIST.dwfilepos": dwfilepos,
        "LIST.protocol": "1",
        "LIST.publicMjCardNo": "1",
        "LIST.MjCardNo": "1",
        "LIST.WgFacility": "",
        "LIST.WgCardID": "",
        "LIST.group": "",
        "LIST.uregno": "0",
        "LIST.uname": name,
        "LIST.ucernumber": "",
        "LIST.ubirth": "2024-01-25",
        "LIST.uphone": "",
        "LIST.uplace": "",
        "LIST.uaddr": "",
        "LIST.uBankNum": "",
        "LIST.utext": text,
        "LIST.uIdCardID": "",
        "LIST.uWardenId": "",
        "LIST.uAccessID": "",
        "LIST.uRoomNum": "",
        "LIST.uRFIdCardNum": rfID_card,
        "LIST.uPassword": "",
        "LIST.uPermission": "0",
        "LIST.uIsCheckSim": 1,
        "LIST.ucardtype": "0",
        "LIST.ulisttype": "0",
        "LIST.ulistChScope": "0",
        "LIST.utype": 0,
        "LIST.usex": gender,
        "LIST.unation": 1,
        "LIST.ucertype": "0",
        "LIST.uStatus": "4",
        "nRanId": nRanId
    }

    try:
        # Sending the POST request with basic authentication
        response = requests.post(url, params=params, auth=HTTPBasicAuth(username, password), timeout=10)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx or 5xx
        
        # Parse the response into JSON
        parsed_data = parse_response_to_json(response.text)
        ic(parsed_data)
        return {
            "status": response.status_code,
            "data": parsed_data
        }
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "The request timed out. Please check the server or try again later."
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"An error occurred: {e}"
        }


# Example usage
# if __name__ == "__main__":
#     try:
#         # Upload an image first
#         data = upload_image(
#             file_path="/Users/m3/Documents/face_id_api/basic_app/services/girl.jpg",
#             ip="192.168.15.20"
#         )
#         ic(data)

#         # Add user with basic authentication
#         result = add_user(
#             ip='192.168.15.20',
#             username='admin',  # Replace with your username
#             password='aifu1q2w3e4r@',  # Replace with your password
#             dwfiletype=data.get('dwfiletype', 0),
#             dwfileindex=data.get('dwfileindex', 1),
#             dwfilepos=data.get('dwfilepos', 0),
#             name="Lisa 1",
#             text="This is a test user",
#             rfID_card=1,
#             nRanId=generate_random_number(),
#             gender=1  # 0 for male, 1 for female
#         )
#         ic(result)
#     except Exception as e:
#         ic(f"An unexpected error occurred: {e}")