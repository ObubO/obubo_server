from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

GENDER = {
        ("M", "MAN"),
        ("W", "WOMAN"),
    }


USERTYPE = {
    ('Self', '본인'),
    ('Guard', '보호자'),
}


class UserManger(BaseUserManager):

    use_in_migration = True

    def _create_user(self, username, nickname, password, **extra_fields):

        if not username:
            raise ValueError("아이디를 입력해주세요")
        if not password:
            raise ValueError('비밀번호를 입력해주세요.')

        username = self.model.normalize_username(username)
        nickname = self.model.normalize_username(nickname)

        user = self.model(username=username, nickname=nickname, **extra_fields)
        user.set_password(password)

        extra_fields.setdefault('is_member', True)

        user.save(using=self.db)

    def create_user(self, username, nickname, password, **extra_fields):

        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, nickname, password, **extra_fields)

    def create_superuser(self, username, nickname, password, **extra_fields):

        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('birth', '2023-05-14')

        return self._create_user(username, nickname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_("username"), max_length=20, validators=[username_validator], unique=True)
    password = models.CharField(_("password"), max_length=255)

    nickname = models.CharField(_("nickname"), max_length=20)
    email = models.EmailField(_("email"), max_length=50, null=True, blank=True)
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER)
    phone = models.CharField(_("phone"), max_length=11, null=True, blank=True)
    birth = models.DateField(_("birth"))
    user_type = models.CharField(_("user_type"), max_length=10, choices=USERTYPE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_member = models.BooleanField(_("member"), default=True)
    refresh_token = models.CharField(_("refresh_token"), max_length=255, null=True, blank=True)

    is_active = models.BooleanField(_("active"), default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManger()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["nickname"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

