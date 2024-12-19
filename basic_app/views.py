from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .models import FaceLog, RFLog

@csrf_exempt
def auth_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        FaceLog.objects.create(
            event_type=data.get('event'),
            user_id=data.get('user_id'),
            name=data.get('name'),
            face_image=data.get('face_image'),
            confidence=data.get('confidence'),
            timestamp=datetime.fromisoformat(data.get('timestamp'))
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def stranger_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        FaceLog.objects.create(
            event_type=data.get('event'),
            face_image=data.get('face_image'),
            confidence=data.get('confidence'),
            timestamp=datetime.fromisoformat(data.get('timestamp'))
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def rf_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        RFLog.objects.create(
            event_type=data.get('event'),
            card_id=data.get('card_id'),
            user_id=data.get('user_id'),
            name=data.get('name'),
            timestamp=datetime.fromisoformat(data.get('timestamp'))
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request"}, status=400)


