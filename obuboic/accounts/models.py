from datetime import date
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from .validators import validate_id, validate_password, validate_name, validate_nickname, validate_phone

GENDER = {
    ("M", "MAN"),
    ("W", "WOMAN"),
}

CONSENT = {
    ('True', '동의'),
    ('False', '비동의'),
}


class UserManger(BaseUserManager):
    use_in_migration = True

    def _create_user(self, username, password, **extra_fields):

        if not username:
            raise ValueError("아이디를 입력해주세요")
        if not password:
            raise ValueError('비밀번호를 입력해주세요.')

        username = self.model.normalize_username(username)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)

        user.save(using=self.db)

        return user

    def create_user(self, username, password, **extra_fields):

        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):

        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_("username"), max_length=20, unique=True, validators=[validate_id])
    password = models.CharField(_("password"), max_length=255, validators=[validate_password])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    refresh_token = models.CharField(_("refresh_token"), max_length=255, null=True, blank=True)

    is_active = models.BooleanField(_("active"), default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManger()

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin


class UserType(models.Model):
    type_name = models.CharField(_("type_name"), max_length=10)

    objects = models.Manager()

    class Meta:
        verbose_name = "회원 유형"

    def __str__(self):
        return self.type_name


class Member(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("name"), max_length=10, validators=[validate_name], null=True, blank=True)
    nickname = models.CharField(_("nickname"), max_length=20, unique=True, validators=[validate_nickname], null=True, blank=True)
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER, null=True, blank=True,)
    birth = models.DateField(_("birth"), null=True, blank=True)
    phone = models.CharField(_("phone"), max_length=11, unique=True, validators=[validate_phone], null=True, blank=True)
    email = models.EmailField(_("email"), max_length=50, unique=True, null=True, blank=True)
    user_type = models.ForeignKey(
        UserType,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "회원 정보"

    def __str__(self):
        return self.name

    def get_gender(self):
        return self.gender


class AuthTable(models.Model):
    phone = models.CharField(_("phone"), max_length=11, validators=[validate_phone])
    code = models.CharField(_("code"), max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.phone


class Terms(models.Model):
    title = models.CharField(_("name"), max_length=20)
    content = models.TextField(_("name"))
    is_necessary = models.BooleanField(_("is_necessary"), default=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "개인정보 이용약관"

    def __str__(self):
        return self.title


class UserTerms(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    terms = models.ForeignKey(
        Terms,
        on_delete=models.CASCADE,
    )
    is_consent = models.CharField(_("is_consent"),max_length=5, choices=CONSENT)
    consent_date = models.DateField(_("consent_date"), auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "약관 동의"

    def __str__(self):
        return self.user.username
