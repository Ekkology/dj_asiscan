from django.db import models

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

from django.contrib.auth.models import User
from django.db import models

class OutstandingToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_outstandingtoken_set')
    token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)