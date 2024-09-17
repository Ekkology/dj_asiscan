from django.shortcuts import render
from django.http import FileResponse
import os
import cv2
import numpy as np
from app_usuarios.models import imagen_preP
from django.http import JsonResponse
import base64



def home(request):
    return render(request,"home.html")

def procesar_imagen():

    foto_64 = obtener_imagen_desde_base_datos()

    foto = decodificar_base64(foto_64)


    # Configuración de rutas
    output_directory = '/home/ekkology/ssd_2'
#output_directory = r'D:\Nueva carpeta\Prueba\IA-de-reconocimiento\PruebasLibrerias\ImagenesProcesadas'


# Cargar el clasificador preentrenado de rostros de OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Cargar la imagen
    image = foto
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detectar rostros
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Dibujar recuadros y guardar imágenes
    for i, (x, y, w, h) in enumerate(faces):
    # Dibujar un recuadro alrededor del rostro
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

# Guardar la imagen con recuadros
    boxed_image_filename = os.path.join(output_directory, 'boxed_image.jpg')


    buffer  = cv2.imwrite(boxed_image_filename, image)
    
    base64_img = base64.b64encode(buffer).decode()
    update_imagen(base64_img)
    print(f"Imagen con recuadros guardada en: {boxed_image_filename}")

    

def send_php_file(request):
    # Ruta completa al archivo PHP
    file_path = os.path.join('php_files', 'script.php')
    
    # Asegúrate de que el archivo exista
    if os.path.exists(file_path):
        # Crea una respuesta con el archivo
        response = FileResponse(open(file_path, 'rb'))
        # Configura el encabezado Content-Type para PHP
        response['Content-Type'] = 'application/x-httpd-php'
        # Define un nombre de archivo sugerido para la descarga (opcional)
        response['Content-Disposition'] = 'attachment; filename="script.php"'
        return response
    else:
        # Si el archivo no existe, devuelve un error 404
        return HttpResponseNotFound('File not found')

def obtener_imagen_desde_base_datos(image_id=1):
    try:
        imagen_base64 = mi_tabla2.objects.values_list('data_base64', flat=True).filter(id=image_id).first()
        return imagen_base64
    except mi_tabla2.DoesNotExist:
        return None


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from app_usuarios.models import imagen_preP

def obtener_imagen(request):
    try:
        # Retrieve the image with id=1
        foto_2 = imagen_preP.objects.get(id=1)
        
        # Extract the base64 data
        data_base64_2 = foto_2.imagen_base64
        if 'base64,' in data_base64_2:
            data_base64_2 = data_base64_2.split('base64,')[1]
        
        # Return the base64 image in JSON response
        return JsonResponse({'imagen_base64_2': data_base64_2})
    except imagen_preP.DoesNotExist:
        # Return an error message if the image doesn't exist
        return JsonResponse({'error': 'No se encontró ninguna imagen en la base de datos'})






def decodificar_base64(base64_str):
    try:
       
        padding = '=' * (4 - len(base64_str) % 4)
        base64_str += padding

        
        if len(base64_str) % 4 != 0:
            print(f"Error: Longitud de cadena base64 no válida. Base64 actual: {base64_str}")
            return None

       
        image_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_data))

        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error decoding base64: {e}")
        return None



def obtener_imagen_desde_base_datos(image_id=1):
    try:
        imagen_base64 = imagen_preP.objects.values_list('data_base64', flat=True).filter(id=image_id).first()
        return imagen_base64
    except mi_tabla2.DoesNotExist:
        return None



def update_imagen(base64_img, image_id=1):
    try:
        reconocimiento_obj = imagen_preP.objects.get(id=image_id)
        reconocimiento_obj.imagen_base64 = base64_img
        reconocimiento_obj.save()
    except reconocimientoBD.DoesNotExist:
        print("Error al actualizar la imagen: El objeto no existe.")
