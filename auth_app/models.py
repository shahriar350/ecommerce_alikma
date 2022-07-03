import random
import string
from datetime import timedelta

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from rest_framework.exceptions import ValidationError

from EcommerceClient.mixins import CUMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, name, phone_number, password, **extra_fields):
        if User.objects.filter(phone_number=phone_number).count() > 0:
            raise ValidationError(_('Phone number is already taken'))
        if not phone_number:
            raise ValidationError(_('Phone number is required'))
        if len(phone_number) != 11:
            raise ValidationError(_('Phone number must be 11 number'))
        if phone_number[0] != '0' and phone_number[1] != '1':
            raise ValidationError(_('Phone number must be start with 01'))
        if not password:
            raise ValidationError(_('Password is required'))
        if not phone_number.isnumeric():
            raise ValidationError(_('Phone number must be numeric'))
        extra_fields.setdefault("active", True)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.name = name.title()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, phone_number, password, **extra_fields):
        extra_fields.setdefault("staff", True)
        extra_fields.setdefault("superuser", True)
        extra_fields.setdefault("admin", True)
        extra_fields.setdefault("active", True)
        user = self.create_user(name, phone_number, password, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    name = models.CharField(_('User name'), max_length=255, null=True, blank=True)
    phone_number = models.CharField(unique=True, max_length=11, validators=[
        RegexValidator(
            regex=r'(^(01)[3-9]\d{8})$',
            message=_('Please provide a valid 11 digit phone number.'),
        ),
    ])
    image = models.ImageField(null=True, blank=True)
    superuser = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "phone_number"

    objects = CustomUserManager()

    @property
    def get_full_name(self):
        return self.name

    @property
    def get_short_name(self):
        return self.name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_first_time(self):
        start = self.date_joined - timedelta(seconds=10)
        end = self.date_joined + timedelta(seconds=10)
        if start <= end:
            return start <= self.updated_at < end
        else:  # over midnight e.g., 23:30-04:15
            return start <= self.updated_at or self.updated_at < end


def key_generator():
    key = ''.join(random.choice(string.digits) for x in range(6))
    if UserOTP.objects.filter(otp=key).exists():
        key = key_generator()
    return key


class UserOTP(CUMixin):
    phone_number = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_otp")
    otp = models.CharField(max_length=6, default=key_generator)
