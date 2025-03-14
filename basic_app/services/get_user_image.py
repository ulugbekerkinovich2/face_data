import requests
from requests.auth import HTTPBasicAuth
# from basic_app.services.gen_random import generate_random_number

def get_user_image(ip, username, password, ranid, dwfiletype, dwfileindex, dwfilepos, output_file):
    """
    Fetches an image from the given IP using Basic Authentication and saves it to a file.

    :param ip: IP address of the server.
    :param username: Username for Basic Authentication.
    :param password: Password for Basic Authentication.
    :param ranid: RanId parameter in the URL.
    :param dwfiletype: File type parameter in the URL.
    :param dwfileindex: File index parameter in the URL.
    :param dwfilepos: File position parameter in the URL.
    :param output_file: Name of the file to save the image to.
    """
    url = (
        f"http://{ip}/webs/getImage?"
        f"action=list&group=IMAGE&dwfiletype={dwfiletype}&dwfileindex={dwfileindex}&dwfilepos={dwfilepos}&RanId={ranid}"
    )

    try:
        # Make a GET request with Basic Authentication
        response = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=10)

        # Check if the request was successful
        response.raise_for_status()

        # Save the image to the specified file
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"Image successfully saved as '{output_file}'.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Example usage
# get_user_image(
#     ip="192.168.15.20",        # Server IP
#     username="admin",          # Basic Auth username
#     password="aifu1q2w3e4r@",  # Basic Auth password
#     ranid=generate_random_number(),             # RanId
#     dwfiletype=0,              # File type (example value, adjust as needed)
#     dwfileindex=1,             # File index (example value, adjust as needed)
#     dwfilepos=8388608,        # File position (example value, adjust as needed)
#     output_file="user_image.jpg"  # Output file name
# )


def get_user_image_log(
    ip, username, password,
    dwfiletype, dwfileindex, dwfilepos, time, output_file
):
    """
     Fetches an image from the given IP using Basic Authentication and saves it to a file.
    
    :param ip: IP address of the server.
    :param username: Username for Basic Authentication.
    :param password: Password for Basic Authentication.
    :param dwfiletype: File type parameter.
    :param dwfileindex: File index parameter.
    :param dwfilepos: File position parameter.
    :param time: Time string in format 'YYYY-MM-DD/HH:MM:SS'
    :param output_file: Path where to save the image.
    """
    url = (
        f"http://{ip}/webs/getImage?"
        f"action=list&group=IMAGE"
        f"&dwfiletype={dwfiletype}"
        f"&dwfileindex={dwfileindex}"
        f"&dwfilepos={dwfilepos}"
        f"&time={time}"  # 🆕 Added time to the query
    )

    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=10)
        response.raise_for_status()

        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"✅ Image successfully saved to '{output_file}'")

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request error occurred: {req_err}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# get_user_image_log(
#     ip="192.168.15.33",
#     username="admin",
#     password="aifu1q2w3e4r@",
#     dwfiletype=2,
#     dwfileindex=1,
#     dwfilepos=76677120,
#     time="2025-03-13/13:40:01",
#     output_file="user_image.jpg"
# )