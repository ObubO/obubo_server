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

PRIVACY_POLICY = {
    ('TERM_OF_USE', '이용약관1'),
    ('PERSONAL_INFORMATION_COLLECT_AGREE', '이용약관2'),
    ('PERSONAL_INFORMATION_UTIL_AGREE', '이용약관3'),
    ('MARKETING_INFORMATION_RECEIVE_AGREE', '이용약관4'),
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

    def create_user(self, username, password, **extra_fields):

        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):

        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('birth', '2023-05-14')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_("username"), max_length=20, validators=[username_validator], unique=True)
    password = models.CharField(_("password"), max_length=255)
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
    type_name = models.CharField(_("user_type"), max_length=10, choices=USERTYPE)
    objects = models.Manager()

    def __str__(self):
        return self.type_name


class Member(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("name"), max_length=20)
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER)
    birth = models.DateField(_("birth"))
    phone = models.CharField(_("phone"), max_length=11, null=True, blank=True)
    email = models.EmailField(_("email"), max_length=50, null=True, blank=True)
    user_type = models.ForeignKey(
        UserType,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "회원정보"

    def __str__(self):
        return self.name


class PrivacyPolicy(models.Model):
    title = models.CharField(_("name"), max_length=20)
    content = models.TextField(_("name"))
    is_necessary = models.BooleanField(_("is_necessary"), default=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "개인정보 이용약관"


class PolicyAgree(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    code = models.ForeignKey(
        PrivacyPolicy,
        on_delete=models.CASCADE,
    )
    is_consent = models.BooleanField(_("is_consent"), default=False)
    consent_date = models.DateTimeField(_("consent_date"), auto_now_add=True)

    class Meta:
        verbose_name = "약관 동의여부"
