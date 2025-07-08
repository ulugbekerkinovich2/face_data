from b2sdk.v1 import *
import time

# 🔐 API ma'lumotlari
KEY_ID = "00527891739006a0000000002"
APP_KEY = "K005OGvy5ItJM9CvQYFabAI5Zls3klk"
BUCKET_NAME = "StatusDeveloper"

# 🌐 B2 API ni tayyorlash
def get_b2_api():
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account("production", KEY_ID, APP_KEY)
    return b2_api

# 1️⃣ ✅ Faylni yuklash funksiyasi
def upload_file_to_b2(local_path: str, b2_path: str):
    b2_api = get_b2_api()
    bucket = b2_api.get_bucket_by_name(BUCKET_NAME)

    bucket.upload_local_file(
        local_file=local_path,
        file_name=b2_path
    )
    print("✅ Fayl yuklandi:", b2_path)
    return b2_path

# 2️⃣ 🔄 Tokenli URL olish funksiyasi
def generate_signed_url(b2_path: str, duration: int = 3600) -> str:
    b2_api = get_b2_api()
    bucket = b2_api.get_bucket_by_name(BUCKET_NAME)

    download_url = b2_api.get_download_url_for_file_name(BUCKET_NAME, b2_path)
    auth_token = bucket.get_download_authorization(
        file_name_prefix=b2_path,
        valid_duration_in_seconds=duration
    )
    signed_url = f"{download_url}?Authorization={auth_token}"
    return signed_url

# ✅ Test qilish
if __name__ == "__main__":
    local_path = "/Users/m3/Documents/face_id_api/media/girl.jpg"
    b2_path = "images/girl.jpg"

    # 1. Upload
    upload_file_to_b2(local_path, b2_path)

    # 2. Link yaratish (1 soatlik)
    signed_url = generate_signed_url(b2_path, duration=3600)
    print("🔗 Signed URL:", signed_url)
