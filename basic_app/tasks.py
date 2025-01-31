import os
import subprocess
import requests
import logging
from django.utils import timezone
from celery import shared_task
from django.conf import settings
from datetime import datetime
from basic_app.services.get_list_menegement import get_list_management
from datetime import datetime
from basic_app.models import UsersManagement
from basic_app.services.get_user import get_user
from django.db.utils import IntegrityError
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Telegram settings
TOKEN = "7850408357:AAFZ8s4Hqjso5XclrAh6xkblW5sOO9O-X9w"  # Replace with your actual bot token
CHAT_ID = -1002355350437  # Replace with your actual chat ID

# Set a password for the ZIP file
ZIP_PASSWORD = "admin-ulugbek-t+Cxe5NY!rc4fmGF"  # Change this to a secure password


@shared_task
def backup_database():
    """
    Celery Task: Backup the database, zip it with a password, and send it to Telegram.
    """
    db_name = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_host = settings.DATABASES['default'].get('HOST', 'localhost')
    db_port = settings.DATABASES['default'].get('PORT', '5432')

    # Get current timestamp for file naming
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Define file paths with timestamp
    backup_file = f"/tmp/{db_name}_backup_{timestamp}.sql"
    zip_file = f"/tmp/{db_name}_backup_{timestamp}.zip"

    try:
        # Step 1: Create Database Backup
        command = f"PGPASSWORD='{db_password}' pg_dump -h {db_host} -p {db_port} -U {db_user} {db_name} > {backup_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"✅ Backup successful: {backup_file}")

        # Step 2: Compress and Add Password to the Backup File
        zip_command = f"zip -P '{ZIP_PASSWORD}' {zip_file} {backup_file}"
        subprocess.run(zip_command, shell=True, check=True)
        print(f"✅ Backup compressed successfully: {zip_file}")

        # Step 3: Send the Encrypted ZIP File to Telegram
        send_to_telegram(zip_file, timestamp)

        # Step 4: Remove the original backup file after zipping
        os.remove(backup_file)
        print("✅ Original backup file deleted after zipping.")

        # Step 5: Remove the ZIP file after sending
        os.remove(zip_file)
        print("✅ ZIP backup file deleted after sending to Telegram.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Backup failed: {e}")


def send_to_telegram(file_path, timestamp):
    """
    Sends the ZIP backup file to Telegram with timestamp.
    """
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(file_path, "rb") as file:
        files = {"document": file}
        data = {
            "chat_id": CHAT_ID,
            "caption": f"📂 **Database Backup** 🗄️\n📅 Date: {timestamp}`"
        }
        response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            print("✅ Backup sent to Telegram successfully.")
        else:
            print(f"❌ Failed to send backup: {response.text}")

@shared_task
def get_list_management_task():
    """
    Celery Task: Fetch users list from multiple devices and insert into the database.
    """
    try:
        face_ids = {
            'ID_2488986': '192.168.15.20',
            'ID_2488993': '192.168.15.27',
            'ID_2488999': '192.168.15.32',
            'ID_2489002': '192.168.15.36',
            'ID_2489005': '192.168.15.39',
            'ID_2489007': '192.168.15.41',
            'ID_2489012': '192.168.15.46',
            'ID_2489019': '192.168.15.53'
        }  # Ensure this is correctly defined in settings.py

        reqcount, begin_time = 1000000, '2024-01-01/00:00:00'
        end_time = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")

        for face_id_, ip in face_ids.items():
            data = get_list_management(ip, reqcount, begin_time, end_time)
            if not data:
                logging.warning(f"⚠️ No data received from {ip} for face_id {face_id_}")
                continue

            for k in data:
                try:
                    name = k.get('uname', "Unknown")
                    if name != "Unknown":
                        name = " ".join(name.split()[:2])  # Take only the first 2 words

                    user_data = get_user(ip, name)
                    face_num = face_id_.split("_")[1]

                    # Ensure required fields exist
                    if "ITEM0.dwfileindex" not in user_data or "ITEM0.dwfiletype" not in user_data:
                        logging.warning(f"⚠️ Missing fields in user data for {name}")
                        continue

                    # Check if the record already exists before inserting
                    existing_entry = UsersManagement.objects.filter(
                        face_id=face_num,
                        uid=int(k.get('uid', 0))
                    ).exists()

                    if existing_entry:
                        logging.info(f"🔄 Skipping duplicate entry for {name} (uid: {k.get('uid', 0)})")
                        continue

                    # Insert new record if it doesn't exist
                    UsersManagement.objects.create(
                        face_id=face_num,
                        uid=int(k.get('uid', 0)),
                        name=name,
                        type=int(k.get('utype', 0)),
                        rf_id_card_num=int(user_data.get('uRFIdCardNum', 0)),
                        gender='male' if k.get('usex', "0") == "0" else "female",
                        extra_info=k.get('utext', ""),
                        dwfiletype=int(k.get('dwfiletype', 0)),
                        dwfileindex=int(k.get('dwfileindex', 0)),
                        dwfilepos=int(k.get('dwfilepos', 0)),
                        time=timezone.make_aware(datetime.strptime(k.get('utime', "2025-01-01/00:00:00"), "%Y-%m-%d/%H:%M:%S"))
                    )

                    logging.info(f"✅ Inserted new user {name} (uid: {k.get('uid', 0)})")

                except IntegrityError:
                    logging.warning(f"⚠️ User {name} (uid: {k.get('uid', 0)}) already exists, skipping insertion.")
                except Exception as e:
                    logging.error(f"❌ Error processing user {k.get('uname', 'Unknown')}: {e}")

    except Exception as e:
        logging.error(f"❌ get_list_management_task encountered an error: {e}")