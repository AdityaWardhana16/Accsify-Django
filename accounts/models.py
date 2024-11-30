from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField('is admin', default=False)
    is_staff = models.BooleanField('is staff', default=False)
    is_pelanggan = models.BooleanField('is pelanggan', default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='images_users/', blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username