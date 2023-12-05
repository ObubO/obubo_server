from django.db import models

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from django.core.mail import send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class UserManger(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, username, password):

        if not email:
            raise ValueError('Email을 입력해주세요.')
        if not password:
            raise ValueError('비밀번호를 입력해주세요.')

        user = self.model(
            email=self.normalize_email(email),
            username=self.model.normalize_username(username),
        )

        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, username, password):

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_("email_address"), max_length=50, unique=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_("username"), max_length=20, validators=[username_validator], blank=True)
    password = models.CharField(_("password"), max_length=1000)

    is_active = models.BooleanField(_("active"), default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManger()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
