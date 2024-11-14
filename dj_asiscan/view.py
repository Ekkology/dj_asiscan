from django.shortcuts import render
from django.http import FileResponse
import os
import cv2
import numpy as np
#from app_usuarios.models import imagen_preP
from django.http import JsonResponse
import base64
import subprocess
import json
import logging
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt
import environ



@csrf_exempt  
def github_webhook(request):

    if request.method == 'GET':  
        
        try:
            subprocess.call(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "C:\\Apache24\\htdocs\\dj_asiscan\\.git\hooks\\post-receive.ps1"])
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'invalid method'}, status=405)  




def home(request):
    return render(request,"home.html")


import base64
from io import BytesIO
from PIL import Image
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse

def generate_image_base64():
    # Aquí puedes crear una imagen en memoria con PIL (Pillow)
    image = Image.new('RGB', (100, 100), color='red')
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def generate_image(request):
    image_base64 = generate_image_base64()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'camera_group', {
            'type': 'send_image',
            'image_data': image_base64
        }
    )
    return HttpResponse(status=200)

def simulate(request):
    return render(request, "display_image.html")