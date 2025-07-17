from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name