import requests
from requests.auth import HTTPBasicAuth
from basic_app.services.gen_random import generate_random_number

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