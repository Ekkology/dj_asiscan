from django.db import models

# Create your models here.
class imagen_preP(models.Model):
    id = models.AutoField(primary_key=True)
    imagen_base64 = models.TextField()

    class Meta:
        db_table = 'imagen_preP'
