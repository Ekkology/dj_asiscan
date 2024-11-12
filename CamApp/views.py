from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Cam, Servo
from django.views.decorators.csrf import csrf_exempt
import logging
import base64
from io import BytesIO
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)
# Create your views here.

@csrf_exempt
def receive_image(request):
    # Si la solicitud es POST, se procesa la imagen
    if request.method == 'POST':
        image_data = request.POST.get('image')
        if image_data:
            image_data = image_data.replace(' ', '+')
            cam, created = Cam.objects.get_or_create(id=1)
            cam.img64 = image_data
            cam.save()
            logger.info("Imagen recibida y almacenada correctamente.")
            
            # Obtener el movimiento del servo
            movimiento = Servo.objects.get(id=1)
            if movimiento is not None:
                return HttpResponse({movimiento})  # Devuelve el código y el movimiento
            
            return HttpResponse("40; No se encontró ningún valor de movimiento", status=400)  # Respuesta de error

        logger.warning("No se recibió ninguna imagen en la solicitud.")
        return HttpResponse("40; No se recibió ninguna imagen", status=400)  # Respuesta de error

    logger.warning("Solicitud no permitida: método no es POST.")
    return HttpResponse("40; Método no permitido", status=405)  # Respuesta de error


def manejar_direccion(request):
    if request.method == 'GET':
        direction = request.GET.get('direction')
        
        if direction:
            # Guardar la dirección en la sesión
            request.session['direction'] = direction
            
            # Obtener el valor de movimiento de la base de datos
            movimiento = Servo.objects.get(id=1)
            
            if movimiento is not None:
                return HttpResponse(movimiento)
    
    return HttpResponse('No se encontró ningún valor de movimiento', status=400)

@csrf_exempt
def display_image(request):
    cam = Cam.objects.filter(id=1).first()

    if cam and cam.img64:
            if cam.img64.startswith('data:image/'):
                base64_image_data = cam.img64.split(',')[1]
            return JsonResponse({'imagen_base64': base64_image_data})
    else:
        return JsonResponse({'error': 'No se encontró ninguna imagen en la base de datos'})

@csrf_exempt
def display_image_view(request):
    return render(request,'display_image.html')
    

#seccion del servo
#enviar valor a la base de datos
@csrf_exempt
def enviar_valor_servos(request):
    if request.method == 'POST':
        movimiento = request.POST.get('movimiento')
        if movimiento:
            try:
                servo = Servo.objects.get(id=1)
                servo.direccion = movimiento
                servo.save()
                return JsonResponse({"message": f"Valor recibido y actualizado: {movimiento}"})
            except Servo.DoesNotExist:
                return JsonResponse({"message": "Error: Servo no encontrado."}, status=404)
        else:
            return JsonResponse({"message": "No se recibió ningún valor."}, status=400)
    
    return JsonResponse({"message": "Método no permitido."}, status=405)
#obtener valor que esta la base de datos del servo
@csrf_exempt
def manejar_direccion(request):
    if request.method == 'GET':
        direction = request.GET.get('direction')
        
        if direction:
            # Guardar la dirección en la sesión
            request.session['direction'] = direction
            
            # Obtener el valor de movimiento de la base de datos
            movimiento = Servo.objects.get(id=1)
            
            if movimiento is not None:
                return HttpResponse(movimiento)
    
    return HttpResponse('No se encontró ningún valor de movimiento', status=400)