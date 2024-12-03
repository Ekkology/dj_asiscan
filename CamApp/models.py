from django.db import models
from django.utils import timezone

# Create your models here.

class Cam (models.Model):
    id = models.AutoField(primary_key=True)
    img64 = models.TextField(null=True, blank=True)
    registro = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.pk:
            self.registro = timezone.now()
        super(Cam, self).save(*args, **kwargs)

    def __str__(self):
        return f"Cam {self.id}"
#seccion del servo
class Servo(models.Model):
    direccion = models.CharField(max_length=3, default='0')
    
    def __str__(self):
        return self.direccion

from django.db import models
from django.utils import timezone
import os
from django.conf import settings

class RecognizedFace(models.Model):
    name = models.CharField(max_length=100)
    confidence = models.FloatField()
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    processed_image = models.ImageField(upload_to='recognized_faces/')
    timestamp = models.DateTimeField(auto_now_add=True)

class UnknownFace(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    processed_image = models.ImageField(upload_to='unknown_faces/')
    timestamp = models.DateTimeField(auto_now_add=True)

