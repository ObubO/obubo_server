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
    username = models.CharField(verbose_name='아이디', max_length=20, unique=True, validators=[validate_id])
    password = models.CharField(verbose_name='비밀번호', max_length=255, validators=[validate_password])
    refresh_token = models.CharField(verbose_name='refresh_token', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_social = models.BooleanField(default=False)

    objects = UserManger()

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    def update_refresh_token(self, refresh):
        """
        A signal receiver which updates the last_login date for
        the user logging in.
        """
        self.refresh_token = refresh
        self.save(update_fields=["refresh_token"])


class UserType(models.Model):
    name = models.CharField(verbose_name='회원유형', max_length=10)

    objects = models.Manager()

    class Meta:
        db_table = 'user_type'
        verbose_name = "회원유형"
        verbose_name_plural = '회원유형 목록'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profiles')
    user_type = models.ForeignKey(UserType, on_delete=models.PROTECT, blank=True, null=True, default=None)

    name = models.CharField(verbose_name='이름', max_length=10, validators=[validate_name], null=True, blank=True)
    nickname = models.CharField(verbose_name='닉네임', max_length=20, unique=True, validators=[validate_nickname], null=True, blank=True)
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDER, null=True, blank=True,)
    birth = models.DateField(verbose_name='생년월일', null=True, blank=True)
    phone = models.CharField(verbose_name='전화번호', max_length=11, unique=True, validators=[validate_phone], null=True, blank=True)
    email = models.EmailField(verbose_name='이메일', max_length=50, unique=True, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = 'user_profile'
        verbose_name = "회원정보"
        verbose_name_plural = '회원정보 목록'

    def __str__(self):
        return self.name

    def get_gender(self):
        return self.gender


class AuthTable(models.Model):
    phone = models.CharField(verbose_name='전화번호', max_length=11, validators=[validate_phone])
    code = models.CharField(verbose_name='인증번호', max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.phone


class Terms(models.Model):
    title = models.CharField(verbose_name='약관명', max_length=20)
    content = models.TextField(verbose_name='약관내용')
    is_necessary = models.BooleanField(verbose_name='필수여부', default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'terms'
        verbose_name = "이용약관"
        verbose_name_plural = "이용약관 목록"

    def __str__(self):
        return self.title


class UserTerms(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    terms = models.ForeignKey(Terms, on_delete=models.CASCADE)
    is_consent = models.CharField(verbose_name='동의여부', max_length=5, choices=CONSENT)
    consent_date = models.DateField(verbose_name='동의날짜', auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'user_terms'
        verbose_name = "이용약관 동의"
        verbose_name_plural = "이용약관 동의 목록"

    def __str__(self):
        return f"[{self.terms}] {self.user.username}"
