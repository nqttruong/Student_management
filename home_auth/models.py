from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.utils.crypto import get_random_string
from django.utils import timezone

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
        related_name = None,
        blank = True
    )
    user_permission = models.ManyToManyField(
        'auth.Permission',
        related_name = None,
        blank = True
    )

    def __str(self):
        return self.username


# lưu thông tin về các yêu cầu reset mật khẩu của người dùng.
class PasswordResetRequest(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    # on_delete = models.CASCADE: nếu user bị xóa → bản ghi reset password này cũng bị xóa theo.
    email = models.EmailField()
    token = models.CharField(max_length=32, default=get_random_string(32), editable=False, unique=True)
    # token: chuỗi ngẫu nhiên dài 32 ký tự → dùng để xác định yêu cầu reset mật khẩu.
    # default=get_random_string(32): mỗi bản ghi tạo ra sẽ có sẵn 1 token random.
    # editable=False: không cho chỉnh sửa trong admin.
    # unique=True: đảm bảo không có 2 token trùng nhau trong DB.
    
    created_at = models.DateTimeField(auto_now_add=True)
    TOKEN_VALIDITY_PERIOD = timezone.timedelta(hours=1)
     
    def is_valid(self):
        return timezone.now() <= self.created_at + self.TOKEN_VALIDITY_PERIOD

    def send_reset_email(self):
        reset_link = f"http://localhost:8000/authentication/reset-password/{self.token}/"
        send_mail(
            'Password Reset Request',
            f'Click the following link to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )