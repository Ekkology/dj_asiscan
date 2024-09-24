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




# Configura el logging
logging.basicConfig(level=logging.INFO)

# Define tu secreto aquí (idealmente, cargado desde variables de entorno)
GITHUB_SECRET = b'mi_secreto_aqui'  # Cambia esto a tu secreto real

@csrf_exempt  # Exime la verificación CSRF para esta vista
def github_webhook(request):
    if request.method == 'POST':
        # Lee el cuerpo de la solicitud
        payload = request.body
        
        # Verifica la firma
        signature = request.META.get('HTTP_X_HUB_SIGNATURE')
        if signature is None:
            logging.error("No signature provided")
            return JsonResponse({'status': 'unauthorized'}, status=401)
        
        # Calcula la firma HMAC
        hash_object = hmac.new(GITHUB_SECRET, payload, hashlib.sha1)
        calculated_signature = 'sha1=' + hash_object.hexdigest()

        # Compara la firma calculada con la firma enviada
        if not hmac.compare_digest(calculated_signature, signature):
            logging.error("Invalid signature")
            return JsonResponse({'status': 'unauthorized'}, status=401)

        # Log para verificar que recibimos el webhook
        payload_data = json.loads(payload)
        logging.info("Webhook received: %s", payload_data)

        # Ejecuta el script de PowerShell
        try:
            subprocess.call(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "C:\\path\\to\\your\\project\\deploy.ps1"])
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logging.error("Error executing script: %s", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'invalid method'}, status=405)










def home(request):
    return render(request,"home.html")


