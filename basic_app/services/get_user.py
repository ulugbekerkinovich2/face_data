import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import re
from icecream import ic
# Django settings dan Basic Auth login ma'lumotlarini olish
# USERNAME = settings.username
# PASSWORD = settings.password
USERNAME = "admin"
PASSWORD = "aifu1q2w3e4r@"
def parse_raw_response(raw_data):
    data_dict = {}
    lines = raw_data.split("\n")

    # Faqat kerakli kalitlarni olish
    required_keys = [
        "sessionid", "beginno", "uRFIdCardNum", 
        "ITEM0.uid", "ITEM0.utype", "ITEM0.uname", "ITEM0.MjCardNo",
        "ITEM0.usex", "ITEM0.unation", "ITEM0.ucertype", "ITEM0.ucernumber",
        "ITEM0.ubirth", "ITEM0.uphone", "ITEM0.uplace", "ITEM0.uaddr",
        "ITEM0.utext", "ITEM0.dwfiletype", "ITEM0.dwfileindex",
        "ITEM0.dwfilepos", "ITEM0.utime"
    ]

    for line in lines:
        match = re.match(r"root\.LIST\.(.+?)=(.*)", line.strip())
        if match:
            key, value = match.groups()
            if key in required_keys:
                data_dict[key] = value if value else None  # Bo'sh qiymatlar uchun None

    return data_dict

def get_user(ip, search_name):
    """
    Foydalanuvchini API orqali qidirish va faqat kerakli ma'lumotlarni JSON formatida qaytarish.

    Args:
        ip (str): Qurilmaning IP manzili (masalan, "192.168.15.20")
        search_name (str): Qidirilayotgan foydalanuvchi ismi (masalan, "Ulugbek")

    Returns:
        dict: JSON formatda faqat kerakli foydalanuvchi ma'lumotlari
    """
    url = (
        f"http://{ip}/webs/getWhitelist?"
        f"action=list&group=LIST&uflag=0&Searchname={search_name}"
        f"&sequence=1&beginno=0&reqcount=20&sessionid=0"
        f"&RanId=62326939&nKeyPassword=0&nPersonalPassword=0"
    )

    try:
        # Basic Authentication bilan GET so'rov jo'natish
        response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()  # HTTP xatoliklarni tekshirish

        # HTML formatdagi javobni kerakli JSON formatga aylantirish
        json_data = parse_raw_response(response.text)

        return json_data  # JSON obyekt qaytarish

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
        return {"error": "HTTP error", "details": str(http_err)}
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request error occurred: {req_err}")
        return {"error": "Request error", "details": str(req_err)}
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {"error": "Unexpected error", "details": str(e)}

# a = get_user(
#     ip="192.168.15.20",
#     search_name="Ulugbek"
# )
# ic(a)