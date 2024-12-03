import json
import logging
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import base64
from datetime import datetime

# Configurar logging
logger = logging.getLogger(__name__)

class CameraConsumer(WebsocketConsumer):
    # Variables de clase compartidas
    last_image = None
    connected_clients = set()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = "camera_group"
        self.is_connected = False

    def connect(self):
        """Maneja la conexi�n inicial del WebSocket."""
        try:
            # Aceptar la conexi�n
            self.accept()
            self.is_connected = True
            
            # A�adir al grupo
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            
            # Registrar este cliente
            self.__class__.connected_clients.add(self.channel_name)
            
            # Enviar la �ltima imagen si existe
            if self.__class__.last_image:
                self.send_image({
                    'image_data': self.__class__.last_image,
                    'timestamp': datetime.now().isoformat()
                })
                
            logger.info(f"Cliente conectado. Total de clientes: {len(self.__class__.connected_clients)}")
            
        except Exception as e:
            logger.error(f"Error en la conexi�n: {str(e)}")
            raise

    def disconnect(self, close_code):
        """Maneja la desconexi�n del WebSocket."""
        try:
            self.is_connected = False
            
            # Eliminar del grupo
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )
            
            # Eliminar de los clientes conectados
            self.__class__.connected_clients.discard(self.channel_name)
            
            logger.info(f"Cliente desconectado. Total de clientes: {len(self.__class__.connected_clients)}")
            
        except Exception as e:
            logger.error(f"Error en la desconexi�n: {str(e)}")
        finally:
            raise StopConsumer()

    def receive(self, text_data=None, bytes_data=None):
        """Maneja los mensajes recibidos."""
        try:
            if not self.is_connected:
                logger.warning("Intento de recibir datos en una conexi�n cerrada")
                return

            if text_data:
                data = json.loads(text_data)
                image_data = data.get('image_data')
                
                if image_data:
                    # Validar el formato base64
                    try:
                        # Verificar que la imagen es v�lida base64
                        base64.b64decode(image_data.split(',')[-1] if ',' in image_data else image_data)
                    except Exception as e:
                        logger.error(f"Datos de imagen inv�lidos: {str(e)}")
                        return

                    # Actualizar la �ltima imagen
                    self.__class__.last_image = image_data
                    
                    # Preparar mensaje con timestamp
                    message = {
                        'type': 'send_image',
                        'image_data': image_data,
                        'timestamp': datetime.now().isoformat()
                    }

                    # Enviar a todos los miembros del grupo
                    async_to_sync(self.channel_layer.group_send)(
                        self.group_name,
                        message
                    )
                    
                    logger.debug("Imagen recibida y distribuida al grupo")

        except json.JSONDecodeError as e:
            logger.error(f"Error decodificando JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Error procesando mensaje: {str(e)}")

    def send_image(self, event):
        """Env�a la imagen a un cliente espec�fico."""
        try:
            if not self.is_connected:
                logger.warning("Intento de enviar datos en una conexi�n cerrada")
                return

            # Extraer datos del evento
            image_data = event.get('image_data')
            timestamp = event.get('timestamp')

            if image_data:
                # Enviar imagen con metadata
                self.send(text_data=json.dumps({
                    'type': 'camera_frame',
                    'image': image_data,
                    'timestamp': timestamp,
                    'clients_connected': len(self.__class__.connected_clients)
                }))
                
        except Exception as e:
            logger.error(f"Error enviando imagen: {str(e)}")
            # No relanzar la excepci�n para mantener la conexi�n viva

    @classmethod
    def broadcast_message(cls, message):
        """M�todo de utilidad para enviar mensajes a todos los clientes conectados."""
        if not cls.connected_clients:
            return
            
        for channel_name in cls.connected_clients:
            try:
                async_to_sync(cls.channel_layer.send)(
                    channel_name,
                    {
                        'type': 'send_image',
                        'image_data': message,
                        'timestamp': datetime.now().isoformat()
                    }
                )
            except Exception as e:
                logger.error(f"Error en broadcast a {channel_name}: {str(e)}")