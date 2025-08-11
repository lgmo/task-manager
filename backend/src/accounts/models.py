from typing import Any

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from common.models.abstract_base_model import AbstractBaseModel


class UserManagerModel(BaseUserManager["UserModel"]):
    def create_user(
        self,
        email: str,
        password: str,
        **extra_fields: Any,  # noqa: ANN401
    ) -> "UserModel":
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields: Any,  # noqa: ANN401
    ) -> "UserModel":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManagerModel()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email

    class Meta:  # pyright: ignore
        app_label = "accounts"
        db_table = "accounts_users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]
