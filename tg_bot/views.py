from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import json

from rest_framework.decorators import api_view

from .bots import process_telegram_event


@api_view(['GET', 'POST'])
def index(request):
    return JsonResponse({"error": "Telegram_proauto"})

class TelegramView(View):
    def post(self, request, *args, **kwargs ):
        process_telegram_event(json.loads(request.body))
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs ):  # for debug
        return JsonResponse({"ok": "Get request processed. But nothing done"})