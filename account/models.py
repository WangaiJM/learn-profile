from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone

class ClinicUser(UserManager):
    def _create_user(self, employee_number, password, **extra_fields):
        if not employee_number:
            raise ValueError('Enter Employee Number')

        user = self.model(employee_number=employee_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, employee_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(employee_number, password, **extra_fields)

    def create_superuser(self, employee_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self._create_user(employee_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    employee_number = models.CharField(max_length=255, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=True)
    username = models.CharField(max_length=255, blank=True, default='')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_labtech = models.BooleanField(default=False)
    is_reception = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = ClinicUser()

    USERNAME_FIELD = 'employee_number'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELD = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username or self.email.split('@')[0]