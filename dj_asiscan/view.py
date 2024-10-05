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


