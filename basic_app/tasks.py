import os
import subprocess
import requests
import logging
from django.utils import timezone
from celery import shared_task
from django.conf import settings
import concurrent.futures
from datetime import datetime
from basic_app.services.get_list_menegement import get_list_management
from basic_app.services.gen_random import generate_random_number
from basic_app.services.get_control_logs import fetch_control_data
from datetime import datetime
from basic_app.models import UsersManagement
from basic_app.services.get_user import get_user
from django.db.utils import IntegrityError
from basic_app.services.get_user_image import get_user_image, get_user_image_log
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from basic_app.models import ControlLog
import time
import os
# import paramiko
import logging
from dotenv import load_dotenv
from celery import shared_task

# .env faylni yuklash (agar ishlatayotgan bo'lsangiz)
load_dotenv()

# Konfiguratsiya
SERVER_HOST = os.getenv("SERVER_HOST", "95.130.227.29")
SERVER_USER = os.getenv("SERVER_USER", "root")
SSH_KEY_PATH = os.path.expanduser("~/.ssh/id_rsa")
REMOTE_MEDIA_PATH = "/var/www/workers/face_data_admin/media"
LOCAL_MEDIA_PATH = "/Users/m3/Documents/face_id_api/media"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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

def process_user(k, ip, face_id_):
    try:
        name = k.get('uname', "Unknown")
        if name != "Unknown":
            name = " ".join(name.split()[:2])

        user_data = get_user(ip, name)
        face_num = face_id_.split("_")[1]

        if "ITEM0.dwfileindex" not in user_data or "ITEM0.dwfiletype" not in user_data:
            logging.warning(f"⚠️ Missing fields in user data for {name}")
            return

        image_filename = f"{name.replace(' ', '_')}_{k.get('uid', 'unknown')}.jpg"
        image_relative_path = os.path.join("images", image_filename)
        image_absolute_path = os.path.join(settings.MEDIA_ROOT, image_relative_path)

        get_user_image(
            ip=ip,
            username="admin",
            password="aifu1q2w3e4r@",
            ranid=generate_random_number(),
            dwfiletype=user_data.get("ITEM0.dwfiletype"),
            dwfileindex=user_data.get("ITEM0.dwfileindex"),
            dwfilepos=user_data.get("ITEM0.dwfilepos"),
            output_file=image_absolute_path
        )

        if not os.path.exists(image_absolute_path):
            logging.warning(f"⚠️ Image download failed for {name}, skipping.")
            return

        user_obj, created = UsersManagement.objects.update_or_create(
            face_id=face_num,
            name=name,
            defaults={
                "uid": int(k.get("uid", 0)),
                "type": int(k.get("utype", 0)),
                "rf_id_card_num": int(user_data.get("uRFIdCardNum", 0)),
                "gender": 'male' if k.get("usex", "0") == "0" else "female",
                "extra_info": k.get("utext", ""),
                "dwfiletype": int(k.get("dwfiletype", 0)),
                "dwfileindex": int(k.get("dwfileindex", 0)),
                "dwfilepos": int(k.get("dwfilepos", 0)),
                "time": timezone.make_aware(datetime.strptime(k.get("utime", "2025-01-01/00:00:00"), "%Y-%m-%d/%H:%M:%S")),
                "image": image_relative_path
            }
        )

        if created:
            logging.info(f"✅ Inserted new user {name} (uid: {k.get('uid', 0)})")
        else:
            logging.info(f"🔄 Updated existing user {name} (uid: {k.get('uid', 0)})")

    except IntegrityError:
        logging.warning(f"⚠️ User {name} (uid: {k.get('uid', 0)}) already exists, skipping insertion.")
    except Exception as e:
        logging.error(f"❌ Error processing user {k.get('uname', 'Unknown')}: {e}")


@shared_task
def get_list_management_task():
    logging.info("🚀 Celery Task Started: Fetching user lists and storing in the database.")

    try:
        face_ids = {
            # 'ID_2488986': '172.16.110.3',
            # 'ID_2488993': '172.16.110.8',
            # 'ID_2488999': '172.16.110.7',
            'ID_2489002': '172.16.110.18',
            'ID_2489005': '172.16.110.23',
            'ID_2489007': '172.16.110.14',
            'ID_2489012': '172.16.110.21',
            'ID_2489019': '172.16.110.15'
        }


        reqcount, begin_time = 100000, '2024-01-01/00:00:00' 
        end_time = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
        image_dir = os.path.join(settings.MEDIA_ROOT, "images")
        os.makedirs(image_dir, exist_ok=True)

        for face_id_, ip in face_ids.items():
            attempts = 0
            data = None

            while attempts < 3 and not data:
                data = get_list_management(ip, reqcount, begin_time, end_time)
                if not data:
                    logging.warning(f"⚠️ Attempt {attempts + 1}: No data received from {ip} for face_id {face_id_}")
                    attempts += 1
                    time.sleep(2)  # 2 soniya kutish (tarmoq yoki server bilan muammo bo'lsa)

            if not data:
                logging.error(f"❌ Failed to get data from {ip} for face_id {face_id_} after 3 attempts.")
                continue

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(process_user, k, ip, face_id_) for k in data]
                for future in concurrent.futures.as_completed(futures):
                    _ = future.result()

    except Exception as e:
        logging.error(f"❌ get_list_management_task encountered an error: {e}")


import os
import json
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from basic_app.models import ControlLog
from basic_app.services.get_user import get_user
from basic_app.services.get_user_image import get_user_image
from basic_app.services.gen_random import generate_random_number
from basic_app.services.get_control_logs import fetch_control_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

import os
import json
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from basic_app.models import ControlLog
from basic_app.services.get_user import get_user
from basic_app.services.get_user_image import get_user_image
from basic_app.services.gen_random import generate_random_number
from basic_app.services.get_control_logs import fetch_all_control_data
from pathlib import Path
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

from basic_app.management.commands.notify_bot import mt_send_group_message
from conf.settings import USERS
from datetime import timedelta
from django.utils import timezone
import redis

# Redis ga ulanish
r = redis.Redis(host='localhost', port=6379, db=0)





@shared_task
def fetch_and_store_control_logs():
    logging.info("🚀 Celery Task Started: Fetching full control logs and storing in the database.")

    face_ids = {
            # 'ID_2488986': '172.16.110.3',
            # 'ID_2488993': '172.16.110.8',
            # 'ID_2488999': '172.16.110.7',
            'ID_2489002': '172.16.110.18',
            'ID_2489005': '172.16.110.23',
            'ID_2489007': '172.16.110.14',
            'ID_2489012': '172.16.110.21',
            'ID_2489019': '172.16.110.15'
        }

    reqcount = 3000
    LAST_RUN_FILE = Path('last_run.txt')

    if LAST_RUN_FILE.exists():
        with open(LAST_RUN_FILE, 'r') as f:
            last_run_str = f.read().strip()
            begintime_dt = datetime.fromisoformat(last_run_str)
            if begintime_dt.tzinfo is None:  # <-- faqat timezone yo‘q bo‘lsa
                begintime_dt = timezone.make_aware(begintime_dt)
    else:
        today = timezone.localdate()
        begintime_dt = timezone.make_aware(datetime.combine(today, datetime.min.time()))


    # 🔁 Hozirgi vaqtni olish
    endtime_dt = timezone.now()

    # 📝 Yangi vaqtni faylga saqlash
    with open(LAST_RUN_FILE, 'w') as f:
        f.write(endtime_dt.isoformat())
    begintime_dt = begintime_dt + timedelta(hours=5)
    endtime_dt = endtime_dt + timedelta(hours=5)
    # ✅ Formatlash
    begintime = begintime_dt.strftime("%Y-%m-%d/%H:%M:%S")
    endtime = endtime_dt.strftime("%Y-%m-%d/%H:%M:%S")

    print("📌 Boshlanish:", begintime)
    print("📌 Tugash:", endtime)




    os.makedirs(os.path.join(settings.MEDIA_ROOT, "controllog"), exist_ok=True)

    def process_control_log(face_id, ip):
        logging.info(f"📥 Starting log processing for face_id: {face_id}, IP: {ip}")

        try:
            output_file = f"/tmp/control_data_{ip.replace('.', '_')}.json"
            sessionid = 0
            ranid = generate_random_number()

            fetch_all_control_data(
                ip=ip,
                username="admin",
                password="aifu1q2w3e4r@",
                ustatus=0,
                usex=2,
                uage="0-100",
                MjCardNo=0,
                begintime=begintime,
                endtime=endtime,
                utype=0,
                sequence=1,
                sessionid=sessionid,
                ranid=ranid,
                output_file=output_file,
                reqcount=reqcount
            )

            if not os.path.exists(output_file):
                logging.warning(f"⚠️ No control data file for {ip}")
                return

            with open(output_file, 'r') as f:
                raw_data = json.load(f)

            logs = raw_data.get("root", {}).get("CONTROL", {})
            logging.info(f"📊 Fetched {len(logs)} logs for {face_id}")

            saved_count = 0
            skipped_count = 0

            for key in logs:
                if not key.startswith("ITEM"):
                    continue

                log_data = logs[key]
                try:
                    name = log_data.get("uname", "Unknown")
                    if name != "Unknown":
                        name = " ".join(name.split()[:2])

                    face_num = int(face_id.split("_")[1])

                    log_time = timezone.make_aware(datetime.strptime(log_data.get("utime", "2025-01-01/00:00:00"), "%Y-%m-%d/%H:%M:%S"))

                    image_filename = f"{name.replace(' ', '_')}_{log_data.get('uid', 'unknown')}.jpg"
                    image_relative_path = os.path.join("controllog", image_filename)
                    image_absolute_path = os.path.join(settings.MEDIA_ROOT, image_relative_path)
                    
                    user_data = get_user(ip, name)

                    get_user_image_log(
                        ip=ip,
                        username="admin",
                        password="aifu1q2w3e4r@",
                        dwfiletype=log_data.get("cfiletype", 0),
                        dwfileindex=log_data.get("cfileindex", 0),
                        dwfilepos=log_data.get("cfilepos", 0),
                        output_file=image_absolute_path,
                        time=log_data.get("utime")
                    )

                    similarity = log_data.get("usimilarity")
                    similarity = float(similarity) if similarity else 0.0

                    existing_log = ControlLog.objects.filter(
                        face_id=face_num,
                        name=name,
                        time=log_time
                    ).first()

                    if existing_log:
                        existing_log.uid = int(log_data.get("uid", 0))
                        existing_log.cfiletype = int(log_data.get("cfiletype", 0))
                        existing_log.cfileindex = int(log_data.get("cfileindex", 0))
                        existing_log.cfilepos = int(log_data.get("cfilepos", 0))
                        existing_log.similarity = int(similarity)
                        existing_log.type = int(log_data.get("utype", 0))
                        existing_log.gender = 'male' if log_data.get("usex", "0") == "0" else "female"
                        existing_log.extra_info = log_data.get("utext", "")
                        existing_log.dwfiletype = int(log_data.get("dwfiletype", 0))
                        existing_log.dwfileindex = int(log_data.get("dwfileindex", 0))
                        existing_log.dwfilepos = int(log_data.get("dwfilepos", 0))
                        existing_log.image = image_relative_path
                        existing_log.save()

                        logging.info(f"🔄 UPDATED — name='{name}', face_id={face_num}, time={log_time}")
                        skipped_count += 1
                        continue

                    special_users = list(settings.USERS.keys())
                    entered_doors = [2489019, 2489007, 2489005, 2488986]

                    try:
                        door_array_index = entered_doors.index(face_num)
                    except ValueError:
                        print(f"Eshik topilmadi: {face_num}")
                        door_array_index = -1
                    # Faylning boshida:


                    # process_control_log ichida:
                    now = timezone.now()
                    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                    seconds_left = int((tomorrow - now).total_seconds())

                    if door_array_index != -1:
                        data = r.get(name)
                        if not data:
                            if name in special_users:
                                mt_send_group_message(...)
                                r.setex(name, seconds_left, door_array_index)




                    ControlLog.objects.create(
                        face_id=face_num,
                        uid=int(log_data.get("uid", 0)),
                        name=name,
                        time=log_time,
                        cfiletype=int(log_data.get("cfiletype", 0)),
                        cfileindex=int(log_data.get("cfileindex", 0)),
                        cfilepos=int(log_data.get("cfilepos", 0)),
                        similarity=int(similarity),
                        type=int(log_data.get("utype", 0)),
                        gender='male' if log_data.get("usex", "0") == "0" else "female",
                        extra_info=log_data.get("utext", ""),
                        dwfiletype=int(log_data.get("dwfiletype", 0)),
                        dwfileindex=int(log_data.get("dwfileindex", 0)),
                        dwfilepos=int(log_data.get("dwfilepos", 0)),
                        image=image_relative_path
                    )

                    logging.info(f"✅ SAVED — name='{name}', face_id={face_num}, time={log_time}")
                    saved_count += 1

                except Exception as e:
                    logging.error(f"❌ ERROR — name='{name}', face_id={face_num}, reason={e}")

            logging.info(f"📦 DONE WITH {face_id}. TOTAL: {len(logs)}, SAVED: {saved_count}, SKIPPED: {skipped_count}")

        except Exception as e:
            logging.error(f"❌ General error in processing face_id {face_id}: {e}")

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(process_control_log, fid, ip) for fid, ip in face_ids.items()]
        for future in as_completed(futures):
            _ = future.result()

    logging.info("✅ Control log task completed.")




# @shared_task
# def upload_then_delete_media_via_sftp():
#     """SFTP orqali fayllarni yuklash va muvaffaqiyatli yuklanganlarini o‘chirish."""
    
#     logger.info("🔄 Fayllarni yuklash jarayoni boshlandi...")
    
#     try:
#         # **1. SSH ulanish**
#         logger.info("🔌 SSH ulanishni boshlayapmiz...")
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Xavfsizlik: Kalitlarni qabul qilish
#         ssh.connect(SERVER_HOST, username=SERVER_USER, key_filename=SSH_KEY_PATH)
#         logger.info("✅ SSH ulanish muvaffaqiyatli!")

#         # **2. SFTP sessiyasini ochish**
#         logger.info("📂 SFTP sessiyasini ochayapmiz...")
#         sftp = ssh.open_sftp()
#         logger.info("✅ SFTP sessiyasi ochildi!")

#         # **3. Fayllarni ko‘rib chiqish**
#         for file_name in os.listdir(LOCAL_MEDIA_PATH):
#             local_file = os.path.join(LOCAL_MEDIA_PATH, file_name)
#             remote_file = os.path.join(REMOTE_MEDIA_PATH, file_name)

#             if os.path.isfile(local_file):
#                 try:
#                     logger.info(f"⬆️ {file_name} yuklanmoqda...")
#                     sftp.put(local_file, remote_file)  # Faylni yuklash
#                     logger.info(f"✅ {file_name} serverga yuklandi!")

#                     # **4. Yuklangan fayl hajmini tekshirish**
#                     remote_size = sftp.stat(remote_file).st_size
#                     local_size = os.path.getsize(local_file)

#                     # if remote_size == local_size:
#                     #     os.remove(local_file)  # Faqat yuklash muvaffaqiyatli bo‘lsa, o‘chiramiz
#                     #     logger.info(f"🗑️ {file_name} lokalda o‘chirildi!")
#                     # else:
#                     #     logger.warning(f"⚠️ {file_name} fayl hajmi mos kelmadi!")

#                 except Exception as file_error:
#                     logger.error(f"❌ {file_name} yuklanmadi! Xatolik: {file_error}")

#         # **5. SFTP va SSH sessiyalarini yopish**
#         logger.info("📴 SFTP va SSH sessiyalarini yopayapmiz...")
#         sftp.close()
#         ssh.close()
#         logger.info("✅ Barcha sessiyalar yopildi!")

#         return "✅ Barcha fayllar yuklandi va lokalda o‘chirildi!"

#     except Exception as e:
#         logger.error(f"❌ Xatolik: {str(e)}")
#         return f"❌ Xatolik: {str(e)}"
