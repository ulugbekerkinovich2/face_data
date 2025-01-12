import base64
import json
from datetime import datetime
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from .models import Heartbeat, VerifyPush, ICCardInfoPush, StrangerCapture

def extract_ip(request):
    """Extract the client IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')

def parse_json(request):
    """Parse JSON body from the request."""
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")

def validate_field(data, field, default=None):
    """Validate and extract a field from a dictionary."""
    return data.get(field, default)

@csrf_exempt
def handle_heartbeat(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)

    ip_address = extract_ip(request)
    print(f"Heartbeat request received from IP: {ip_address}")

    try:
        data = parse_json(request)
        info = validate_field(data, "info")
        if not info:
            return JsonResponse({"error": "Missing 'info' in request data"}, status=400)

        raw_time = parse_datetime(info["Time"])
        aware_time = make_aware(raw_time)
        
        Heartbeat.objects.create(
            device_id=info["DeviceID"],
            ip_address=validate_field(info, "Ip", "Unknown"),
            mac_address=validate_field(info, "MacAddr", ""),
            time=aware_time
        )
        return JsonResponse({"status": "success", "message": "Heartbeat saved successfully"}, status=200)

    except Exception as e:
        print(f"Error in handle_heartbeat: IP={ip_address}, ERROR={e}")
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def handle_verify_push(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)

    ip_address = extract_ip(request)
    print(f"VerifyPush request received from IP: {ip_address}")

    try:
        data = parse_json(request)
        info = validate_field(data, "info")
        if not info:
            return JsonResponse({"error": "Missing 'info' in request data"}, status=400)

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
            id_card=info.get("IdCard", "").strip() or None,
            birthday=parse_datetime(info["Birthday"]).date() if info["Birthday"] else None,
            telnum=info.get("Telnum", "").strip() or None,
            native=info.get("Native", "").strip() or None,
            address=info.get("Address", "").strip() or None,
            notes=info.get("Notes", "").strip() or None,
            mj_card_from=info["MjCardFrom"],
            mj_card_no=info["MjCardNo"],
            rfid_card=info["RFIDCard"],
            tempvalid=info["Tempvalid"],
            customize_id=info["CustomizeID"],
            person_uuid=info.get("PersonUUID", "").strip() or None,
            valid_begin=parse_datetime(info["ValidBegin"]) if info["ValidBegin"] != "0000-00-00T00:00:00" else None,
            valid_end=parse_datetime(info["ValidEnd"]) if info["ValidEnd"] != "0000-00-00T00:00:00" else None,
            send_in_time=info["Sendintime"],
            direction=info["Direction"],
            sz_qr_code_data=info["szQrCodeData"],
            ip_address=ip_address
        )
        return JsonResponse({"status": "success", "message": "VerifyPush saved successfully", "verify_push_id": verify_push.id}, status=200)

    except KeyError as e:
        return JsonResponse({"error": f"Missing key: {e}"}, status=400)
    except Exception as e:
        print(f"Error in handle_verify_push: IP={ip_address}, ERROR={e}")
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def handle_ic_card_info_push(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)

    ip_address = extract_ip(request)
    print(f"ICCardInfoPush request received from IP: {ip_address}")

    try:
        data = parse_json(request)
        info = validate_field(data, "info")
        if not info:
            return JsonResponse({"error": "Missing 'info' in request data"}, status=400)

        ic_card_info = ICCardInfoPush.objects.create(
            device_id=info.get("DeviceID"),
            ic_card_num=info.get("ICCardNum"),
            created_at=parse_datetime(info.get("CreateTime")),
            ip_address=ip_address,
        )
        return JsonResponse({"status": "success", "message": "ICCardInfoPush saved successfully", "ic_card_info_id": ic_card_info.id}, status=200)

    except Exception as e:
        print(f"Error in handle_ic_card_info_push: IP={ip_address}, ERROR={e}")
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def handle_stranger_capture(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)

    try:
        data = parse_json(request)
        base64_image = data.get("SanpPic")
        info = validate_field(data, "info")
        ip_address = validate_field(info, "ip_address")
        print(f"StrangerCapture request: IP={ip_address}, Data={data}")

        if not base64_image or not info:
            return JsonResponse({"error": "Missing 'SanpPic' or 'info' in request data"}, status=400)

        if base64_image.startswith("data:image"):
            _, base64_image = base64_image.split(",", 1)

        decoded_image = base64.b64decode(base64_image)
        image_filename = f"{info['DeviceID']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"

        stranger_capture = StrangerCapture(
            create_time=parse_datetime(info["CreateTime"]),
            device_id=info["DeviceID"],
            direction=info["Direction"],
            picture_type=info["PictureType"],
            send_in_time=info["Sendintime"],
            operator=data["operator"],
            ip_address=ip_address
        )
        stranger_capture.image_file.save(image_filename, ContentFile(decoded_image), save=True)
        
        return JsonResponse({"status": "success", "message": "StrangerCapture saved successfully", "image_url": stranger_capture.image_file.url}, status=200)

    except Exception as e:
        print(f"Error in handle_stranger_capture: ERROR={e}")
        return JsonResponse({"error": str(e)}, status=500)
