import threading
from django.core.mail import send_mail
from django.conf import settings

def enviar_correo_asincrono(destinatario, asunto, mensaje):
    thread = threading.Thread(target=send_mail, args=(
        asunto,
        mensaje,
        settings.EMAIL_HOST_USER,  
        [destinatario],  
    ))
    thread.start()