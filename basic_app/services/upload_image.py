import requests
from basic_app.services.gen_random import generate_random_number


def parse_response(data):
    """
    Parse the response to extract only required fields.
    """
    lines = data.split("\n")
    result = {}
    for line in lines:
        if "dwfiletype" in line:
            result["dwfiletype"] = line.split("=")[-1].strip()
        elif "dwfileindex" in line:
            result["dwfileindex"] = line.split("=")[-1].strip()
        elif "dwfilepos" in line:
            result["dwfilepos"] = line.split("=")[-1].strip()
        elif "uname" in line:
            result["uname"] = line.split("=")[-1].strip()
    return result


def get_file_size(ip, ranID):
    """
    Retrieve file size and status information from the server.
    """
    url = f"http://{ip}/webs/getUploadPercent?action=list&group=UPLOAD&sessionid={ranID}&nRanId={generate_random_number()}"
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        return "Connection timed out. Please check the IP address and network connectivity."
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching file size: {e}"


def upload_image(ip, file_path):
    """
    Upload an image file to the server and retrieve its upload details.
    """
    ranID = generate_random_number()
    url = f"http://{ip}/webs/uploadfile?action=LISTADD&group=UPLOAD&sessionid={ranID}&IsCheckSim=0"

    try:
        # Use a context manager to ensure the file is properly closed
        with open(file_path, 'rb') as file:
            files = {'txt': file}
            data = {'vfileselector': '(binary)'}
            
            # Post the file to the server
            response = requests.post(url, files=files, data=data, timeout=10)
            response.raise_for_status()
            
            # If the upload is successful, fetch file size details
            raw_data = get_file_size(ip, ranID)
            
            # Parse and return the extracted fields
            parsed_data = parse_response(raw_data)
            return parsed_data

    except requests.exceptions.Timeout:
        return {'message': "Connection timed out. Please check the IP address and network connectivity.", "status": 400}
    except requests.exceptions.RequestException as e:
        return {'message': f"An error occurred: {e}", "status": 400}
    except FileNotFoundError:
        return {'message': "File not found. Please check the file path.", "status": 404}
    except Exception as e:
        return {'message': f"An unexpected error occurred: {e}", "status": 500}


# Example usage
# if __name__ == "__main__":
#     ip_address = "192.168.15.20"
#     file_path = "user_image.jpg"
#     result = upload_image(ip_address, file_path)
#     print(result)



def send_image_to_controllog(id: int, image_path: str):
    url = "http://127.0.0.1:8189/update_image_controllog"
    with open(image_path, 'rb') as img:
        files = {'image': img}
        data = {'id': id}
        response = requests.post(url, data=data, files=files, timeout=90)
    
    try:
        response.raise_for_status()
        print("✅ Controllog javobi:", response.json())
    except requests.RequestException as e:
        print("❌ Xatolik:", e)

def send_image_to_management(id: int, image_path: str):
    url = "https://face-id-admin.misterdev.uz/update_image_management"
    with open(image_path, 'rb') as img:
        files = {'image': img}
        data = {'id': id}
        response = requests.post(url, data=data, files=files)

    try:
        response.raise_for_status()
        print("✅ Management javobi:", response.json())
    except requests.RequestException as e:
        print("❌ Xatolik:", e)