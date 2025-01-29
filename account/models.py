import os
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        try:
            if not email:
                raise ValueError(_("The Email must be set"))
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(f"Error creating user: {str(e)}")

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_("email address"), unique=True, max_length=200, blank=False, null=False)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    username = None
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-create_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"