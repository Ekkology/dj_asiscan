from django.apps import AppConfig

class AppUsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_usuarios'

    def ready(self):
        pass # Importa el archivo de señales
