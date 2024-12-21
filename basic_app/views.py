import base64
import json
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from datetime import datetime
from .models import Heartbeat, VerifyPush, ICCardInfoPush, StrangerCapture
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def handle_heartbeat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            info = data.get("info")
            print(info)
            # Validate inputs
            if not info:
                return JsonResponse({"error": "Invalid data provided"}, status=400)
            print(info["Time"])
            # Save Heartbeat data
            Heartbeat.objects.create(
                device_id=info["DeviceID"],
                ip_address=info["Ip"],
                mac_address=info["MacAddr"],
                time=parse_datetime(info["Time"]),
            )
            return JsonResponse({"status": "success", "message": "Heartbeat saved successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)

@csrf_exempt
def handle_verify_push(request):
    if request.method == "POST":
        try:
            # JSON ma'lumotlarni olish
            data = json.loads(request.body)
            info = data.get("info")

            # Kiritilgan ma'lumotlarni tekshirish
            if not info:
                return JsonResponse({"error": "Invalid data provided"}, status=400)

            # print("Verify pushdan keldi:", info)

            # VerifyPush ma'lumotlarini saqlash
            verify_push = VerifyPush.objects.create(
                person_id=info["PersonID"],
                create_time=parse_datetime(info["CreateTime"]),
                similarity1=info["Similarity1"],
                similarity2=info["Similarity2"],
                verify_status=info["VerifyStatus"],
                verify_type=info["VerfyType"],
                person_type=info["PersonType"],
                name=info["Name"],
                gender=info["Gender"],
                nation=info["Nation"],
                card_type=info["CardType"],
                id_card=info["IdCard"].strip() if info["IdCard"] else None,
                birthday=parse_datetime(info["Birthday"]).date() if info["Birthday"] else None,
                telnum=info["Telnum"].strip() if info["Telnum"] else None,
                native=info["Native"].strip() if info["Native"] else None,
                address=info["Address"].strip() if info["Address"] else None,
                notes=info["Notes"].strip() if info["Notes"] else None,
                mj_card_from=info["MjCardFrom"],
                mj_card_no=info["MjCardNo"],
                rfid_card=info["RFIDCard"],
                tempvalid=info["Tempvalid"],
                customize_id=info["CustomizeID"],
                person_uuid=info["PersonUUID"].strip() if info["PersonUUID"] else None,
                valid_begin=parse_datetime(info["ValidBegin"]) if info["ValidBegin"] != "0000-00-00T00:00:00" else None,
                valid_end=parse_datetime(info["ValidEnd"]) if info["ValidEnd"] != "0000-00-00T00:00:00" else None,
                send_in_time=info["Sendintime"],
                direction=info["Direction"],
                sz_qr_code_data=info["szQrCodeData"],
            )

            return JsonResponse(
                {"status": "success", "message": "VerifyPush saved successfully", "verify_push_id": verify_push.id},
                status=200,
            )

        except KeyError as e:
            return JsonResponse({"error": f"Missing key: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)

@csrf_exempt
def handle_ic_card_info_push(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            info = data.get("info")
            # print(info)
            # Validate inputs
            if not info:
                return JsonResponse({"error": "Invalid data provided"}, status=400)

            # Save ICCardInfoPush data
            ICCardInfoPush.objects.create(
                device_id=info["DeviceID"],
                ic_card_num=info["ICCardNum"],
            )
            return JsonResponse({"status": "success", "message": "ICCardInfoPush saved successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)

@csrf_exempt
def handle_stranger_capture(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            base64_image = data.get("SanpPic")
            info = data.get("info")

            # Validate inputs
            if not base64_image or not info:
                return JsonResponse({"error": "Invalid data provided"}, status=400)

            # Decode base64 image
            if base64_image.startswith("data:image"):
                header, base64_image = base64_image.split(",", 1)

            decoded_image = base64.b64decode(base64_image)
            image_filename = f"{info['DeviceID']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"

            # Save StrangerCapture data
            stranger_capture = StrangerCapture(
                create_time=parse_datetime(info["CreateTime"]),
                device_id=info["DeviceID"],
                direction=info["Direction"],
                picture_type=info["PictureType"],
                send_in_time=info["Sendintime"],
                operator=data["operator"],
            )
            stranger_capture.image_file.save(image_filename, ContentFile(decoded_image), save=True)

            return JsonResponse({
                "status": "success",
                "message": "StrangerCapture saved successfully",
                "image_url": stranger_capture.image_file.url
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)
