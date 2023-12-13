from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

GENDER = {
        ("M", "Man"),
        ("W", "Woman"),
    }


class UserManger(BaseUserManager):

    use_in_migration = True

    def _create_user(self, login_id, username, password, **extra_fields):

        if not login_id:
            raise ValueError("아이디를 입력해주세요")
        if not password:
            raise ValueError('비밀번호를 입력해주세요.')

        login_id = self.model.normalize_username(login_id)
        username = self.model.normalize_username(username)

        user = self.model(login_id=login_id, username=username, **extra_fields)
        user.set_password(password)

        user.save(using=self.db)

    def create_user(self, login_id, username, password, **extra_fields):

        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(login_id, username, password, **extra_fields)

    def create_superuser(self, login_id, username, password, **extra_fields):

        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(login_id, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    login_id = models.CharField(_("login_id"), max_length=50, unique=True)

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_("username"), max_length=20, validators=[username_validator], blank=True)

    password = models.CharField(_("password"), max_length=255)

    gender = models.CharField(_("gender"), max_length=1, choices=GENDER)

    phone = models.CharField(_("phone"), max_length=11, null=True, blank=True)

    birth = models.DateField(_("birth"), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateField(auto_now=True)

    is_active = models.BooleanField(_("active"), default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManger()

    USERNAME_FIELD = "login_id"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.login_id

    @property
    def is_staff(self):
        return self.is_admin
