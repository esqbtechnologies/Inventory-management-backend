from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager


# Options of role of USER
role_choice = (
    ('General_manager', 'General_manager'),
    ('Store_manager', 'Store_manager'),
    ('Worker', 'Worker'),
)


class MyUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Email must be provided')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User model


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(
        max_length=100, choices=role_choice, default='Worker')

    date_joined = models.DateTimeField(default=timezone.now)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __getitem__(self, key):
        return getattr(self, key)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
