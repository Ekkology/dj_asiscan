from django.db import models

class imagen_preP(models.Model):
    id = models.AutoField(primary_key=True)
    imagen_base64 = models.TextField()

    class Meta:
        db_table = 'imagen_preP'




class User(models.Model):
    
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auth_user'  
        managed = False  

    def __str__(self):
        return self.username
