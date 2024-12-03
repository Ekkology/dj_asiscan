from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Cam, Servo
from django.views.decorators.csrf import csrf_exempt
import logging
import base64
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)
# Create your views here.

#@csrf_exempt
# def receive_image(request):
#     # Si la solicitud es POST, se procesa la imagen
#     if request.method == 'POST':
#         image_data = request.POST.get('image')
#         if image_data:
#             image_data = image_data.replace(' ', '+')
#             cam, created = Cam.objects.get_or_create(id=1)
#             cam.img64 = image_data
#             cam.save()
#             logger.info("Imagen recibida y almacenada correctamente.")
            
#             # Obtener el movimiento del servo
#             movimiento = Servo.objects.get(id=1)
#             if movimiento is not None:
#                 return HttpResponse({movimiento})  # Devuelve el código y el movimiento
            
#             return HttpResponse("40; No se encontró ningún valor de movimiento", status=400)  # Respuesta de error

#         logger.warning("No se recibió ninguna imagen en la solicitud.")
#         return HttpResponse("40; No se recibió ninguna imagen", status=400)  # Respuesta de error

#     logger.warning("Solicitud no permitida: método no es POST.")
#     return HttpResponse("40; Método no permitido", status=405)  # Respuesta de error
@csrf_exempt
def receive_image(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')
        if image_data:
            image_data = image_data.replace(' ', '+')

            # Enviar la imagen a través de WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "camera_group", {
                    "type": "send_image",
                    "image_data": image_data
                }
            )
            
           # logger.info("Imagen recibida y enviada a través del WebSocket.")
            #return HttpResponse("Imagen recibida y enviada correctamente.")
                    # Obtener el movimiento del servo
            movimiento = Servo.objects.get(id=1)
            if movimiento is not None:
                return HttpResponse({movimiento})  # Devuelve el c�digo y el movimiento
            
           
            return HttpResponse("40; No se encontro ningun valor de movimiento", status=400)  # Respuesta de error
        
        logger.warning("No se recibió ninguna imagen en la solicitud.")
        return HttpResponse("No se recibió ninguna imagen", status=400)

    logger.warning("Solicitud no permitida: método no es POST.")
    return HttpResponse("Método no permitido", status=405)

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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import base64
from django.conf import settings




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import base64
import os
from django.utils import timezone
from django.conf import settings
from .models import RecognizedFace , UnknownFace

@csrf_exempt
@require_http_methods(["POST"])
def process_face_recognition(request):
    """
    Handle face recognition results from the Python script and save results to JSON
    """
    try:
        # Parse incoming JSON data
        data = json.loads(request.body)
        
        # Get raw data before processing
        verified_faces = data.get('verified', [])
        pending_faces = data.get('pending', [])
        unknown_faces = data.get('unknown', [])
        encoded_image = data.get('image', '')
        
        # Prepare result JSON maintaining original structure
        result = {
            'verified': verified_faces,
            'pending': pending_faces,
            'unknown': unknown_faces,
            'image': encoded_image
        }
        
        # Process data for database if needed
        filename = None
        if encoded_image:
            # Save image to media directory
            image_data = base64.b64decode(encoded_image)
            filename = f"processed_image_{timezone.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            
            with open(os.path.join(settings.MEDIA_ROOT, filename), 'wb') as f:
                f.write(image_data)
        
        # Create database records for recognized faces
        recognized_faces = []
        for face in verified_faces:
            recognized_face = RecognizedFace.objects.create(
                name=face.get('name_person', 'Unknown'),
                confidence=1 - face.get('distance', 0),
                x=face.get('facial_area', {}).get('x', 0),
                y=face.get('facial_area', {}).get('y', 0),
                width=face.get('facial_area', {}).get('w', 0),
                height=face.get('facial_area', {}).get('h', 0),
                processed_image=filename
            )
            recognized_faces.append(recognized_face)
        
        # Create database records for unknown faces
        for face in unknown_faces:
            UnknownFace.objects.create(
                x=face.get('facial_area', {}).get('x', 0),
                y=face.get('facial_area', {}).get('y', 0),
                width=face.get('facial_area', {}).get('w', 0),
                height=face.get('facial_area', {}).get('h', 0),
                processed_image=filename
            )
        
        # Save complete result JSON (including base64 image)
        result_filename = f"face_recognition_result_{timezone.now().strftime('%Y%m%d_%H%M%S')}.json"
        result_path = os.path.join(settings.MEDIA_ROOT, 'face_recognition_result', result_filename)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(result_path), exist_ok=True)
        
        # Save the result JSON maintaining original structure
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False)
        
        return JsonResponse({
            'status': 'success',
            'verified_count': len(verified_faces),
            'pending_count': len(pending_faces),
            'unknown_count': len(unknown_faces),
            'result_file': result_filename
        })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
# views.py
from django.shortcuts import render
from .models import RecognizedFace, UnknownFace
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

# # views.py
# from django.shortcuts import render
# from .models import RecognizedFace, UnknownFace
# from django.db.models import Count
# from django.utils import timezone
# from datetime import timedelta

# def face_recognition_dashboard(request):
#     # Obtener todas las caras reconocidas ordenadas por fecha
#     recognized_faces = RecognizedFace.objects.all().order_by('-timestamp')
#     unknown_faces = UnknownFace.objects.all().order_by('-timestamp')

#     # Estad�sticas generales
#     total_recognized = recognized_faces.count()
#     total_unknown = unknown_faces.count()
    
#     # Obtener estadasticas de los ultimos 7 d�as
#     last_week = timezone.now() - timedelta(days=7)
#     daily_stats = RecognizedFace.objects.filter(
#         timestamp__gte=last_week
#     ).extra({
#         'day': "DATE(timestamp)"
#     }).values('day').annotate(
#         recognized_count=Count('id')
#     ).order_by('day')

#     # Personas mas frecuentes
#     frequent_people = RecognizedFace.objects.values('name').annotate(
#         count=Count('id')
#     ).order_by('-count')[:5]

#     context = {
#         'recognized_faces': recognized_faces[:10],  # ultimas 10 detecciones
#         'unknown_faces': unknown_faces[:10],        # ultimas 10 caras desconocidas
#         'total_recognized': total_recognized,
#         'total_unknown': total_unknown,
#         'daily_stats': daily_stats,
#         'frequent_people': frequent_people,
#     }
    
#     return render(request, 'display_image.html', context)




# views.py
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FaceRecognitionView(View):
    template_name = 'results.html'
    
    def __init__(self):
        super().__init__()
        self.results_dir = os.path.join(settings.MEDIA_ROOT, 'face_recognition_result')
        os.makedirs(self.results_dir, exist_ok=True)
    
    def get_latest_file(self):
        """Helper method to safely get the latest JSON file"""
        try:
            json_files = [f for f in os.listdir(self.results_dir) 
                         if f.endswith('.json')]
            
            if not json_files:
                return None
                
            # Ordenar por fecha de modificaci�n en lugar de nombre
            json_files.sort(key=lambda x: os.path.getmtime(
                os.path.join(self.results_dir, x)), reverse=True)
            
            return json_files[0] if json_files else None
            
        except Exception as e:
            logger.error(f"Error getting latest file: {str(e)}")
            return None

    def list_directory_contents(self):
        """Helper method to list directory contents for debugging"""
        try:
            all_files = os.listdir(self.results_dir)
            json_files = [f for f in all_files if f.endswith('.json')]
            
            # Añadir informacion de fecha de modificaci�n
            json_files_info = []
            for f in json_files:
                file_path = os.path.join(self.results_dir, f)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                json_files_info.append({
                    'name': f,
                    'modified': mod_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'size': os.path.getsize(file_path)
                })
            
            return {
                'directory': self.results_dir,
                'all_files': all_files,
                'json_files': json_files_info,
                'exists': os.path.exists(self.results_dir),
                'is_dir': os.path.isdir(self.results_dir),
                'total_files': len(all_files),
                'total_json_files': len(json_files)
            }
        except Exception as e:
            return {'error': str(e)}

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'face_recognition_results_{timestamp}.json'
            filepath = os.path.join(self.results_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            logger.info(f"Archivo guardado exitosamente en: {filepath}")
            
            return JsonResponse({
                'status': 'success',
                'filename': filename,
                'filepath': filepath,
                'directory_info': self.list_directory_contents()
            })
            
        except Exception as e:
            logger.error(f"Error en POST: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e),
                'directory_info': self.list_directory_contents()
            }, status=400)
    
    def get(self, request, *args, **kwargs):
        try:
            directory_info = self.list_directory_contents()
            latest_file = self.get_latest_file()
            
            if not latest_file:
                return render(request, self.template_name, {
                    'error': 'No hay archivos JSON disponibles en el directorio',
                    'directory_info': directory_info,
                    'debug_mode': settings.DEBUG
                })
            
            filepath = os.path.join(self.results_dir, latest_file)
            logger.info(f"Intentando leer archivo: {filepath}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Obtener la fecha de modificacion del archivo
            timestamp = datetime.fromtimestamp(os.path.getmtime(filepath))
            
            context = {
                'verified_faces': data.get('verified', []),
                'unknown_faces': data.get('unknown', []),
                'pending_faces': data.get('pending', []),
                'image_base64': data.get('image', ''),
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'directory_info': directory_info,
                'debug_mode': settings.DEBUG,
                'current_file': latest_file
            }
            
            return render(request, self.template_name, context)
            
        except Exception as e:
            logger.error(f"Error en GET: {str(e)}")
            return render(request, self.template_name, {
                'error': f"Error al procesar los resultados: {str(e)}",
                'directory_info': self.list_directory_contents(),
                'debug_mode': settings.DEBUG
            })
        
# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.conf import settings
import os
import json
from datetime import datetime
from .serializer import *

# class FaceRecognitionViewSet(viewsets.ViewSet):
#     def list(self, request):
#         """
#         Obtiene los �ltimos resultados de reconocimiento facial
#         """
#         try:
#             # Directorio donde se guardan los resultados
#             result_dir = os.path.join(settings.MEDIA_ROOT, 'face_recognition_result')
            
#             # Obtener el archivo m�s reciente
#             files = os.listdir(result_dir)
#             if not files:
#                 return Response({'message': 'No hay resultados disponibles'}, 
#                               status=status.HTTP_404_NOT_FOUND)
                
#             latest_file = max(files, key=lambda x: os.path.getctime(
#                 os.path.join(result_dir, x)))
            
#             # Leer el archivo JSON
#             with open(os.path.join(result_dir, latest_file), 'r') as f:
#                 data = json.load(f)
                
#             # Agregar timestamp basado en el nombre del archivo
#             timestamp_str = latest_file.split('_')[-1].split('.')[0]
#             data['timestamp'] = datetime.strptime(
#                 timestamp_str, '%Y%m%d%H%M%S')
            
#             # Serializar y retornar
#             serializer = FaceRecognitionResultSerializer(data=data)
#             if serializer.is_valid():
#                 return Response(serializer.validated_data)
#             return Response(serializer.errors, 
#                           status=status.HTTP_400_BAD_REQUEST)
            
#         except Exception as e:
#             return Response(
#                 {'error': str(e)}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
    
#     @action(detail=False, methods=['get'])
#     def history(self, request):
#         """
#         Obtiene el historial de reconocimientos faciales
#         """
#         try:
#             result_dir = os.path.join(settings.MEDIA_ROOT, 'face_recognition_result')
#             files = os.listdir(result_dir)
#             results = []
            
#             for file in sorted(files, reverse=True)[:10]:  # �ltimos 10 resultados
#                 with open(os.path.join(result_dir, file), 'r') as f:
#                     data = json.load(f)
#                     # Agregar timestamp basado en el nombre del archivo
#                     timestamp_str = file.split('_')[-1].split('.')[0]
#                     data['timestamp'] = datetime.strptime(
#                         timestamp_str, '%Y%m%d%H%M%S')
#                     results.append(data)
            
#             serializer = FaceRecognitionResultSerializer(results, many=True)
#             return Response(serializer.data)
            
#         except Exception as e:
#             return Response(
#                 {'error': str(e)}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
class FaceRecognitionViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        Obtiene el �ltimo resultado de reconocimiento facial
        """
        try:
            # Obtener el archivo JSON m�s reciente
            result_dir = os.path.join(settings.MEDIA_ROOT, 'face_recognition_result')
            files = os.listdir(result_dir)
            if not files:
                return Response({'message': 'No hay resultados disponibles'})
                
            latest_file = max(files, key=lambda x: os.path.getctime(
                os.path.join(result_dir, x)))
            
            # Leer y retornar el JSON tal cual est�
            with open(os.path.join(result_dir, latest_file), 'r') as f:
                data = json.load(f)
                
            return Response(data)
            
        except Exception as e:
            return Response({'error': str(e)})
