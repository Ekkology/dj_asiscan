from django.db import models

# Create your models here.
 
#Campos que debe contener la tabla de reportes 

class reportes(models.Model):
 
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField()
    usuario = models.ForeignKey('app_usuarios.User', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='reportes/')
    comentarios = models.ManyToManyField('app_usuarios.User', related_name='comentarios')

    def __str__(self):
      return self.nombre