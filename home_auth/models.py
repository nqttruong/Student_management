from django.db import models
from typing_extensions import AbstractUser
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add = True)
    is_authorized = models.BooleanField(default=False)

    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name = True,
        blank = True
    )
    user_permission = models.ManyToManyField(
        'auth.Permission',
        related_name = None,
        blank = True
    )

    def __str(self):
        return self.username

class PasswordResetRequest(models.Model):
    user = models.Foreignkey('CustomUser', on_delete=models.CASCADE)
    email = models.EmailField()
    token = models.CharField(max_length=32, default=get_random_string(32), editable=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
