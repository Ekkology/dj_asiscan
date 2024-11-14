import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class CameraConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # Agregar al grupo para manejar múltiples conexiones si es necesario
        async_to_sync(self.channel_layer.group_add)("camera_group", self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("camera_group", self.channel_name)

    def send_image(self, event):
        image_data = event['image_data']
        self.send(text_data=json.dumps({
            'image': image_data
        }))
