import re
from django.core.exceptions import ValidationError


def validate_id(value):
    if not re.match(r'^(?=.*[a-z0-9])[a-z0-9]{4,16}$', value):
        raise ValidationError(
            '4자 이상 16자 이하, 영어 또는 숫자로 구성',
            params={'value': value},
        )


def validate_password(value):
    if not re.match(r'^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{8,15}$', value):
        raise ValidationError(
            '8자 이상 20자 이하, 영어 또는 숫자로 구성',
            params={'value': value},
        )


def validate_name(value):
    None


def validate_nickname(value):
    if not re.match(r'^([a-zA-Z0-9ㄱ-ㅎ|ㅏ-ㅣ|가-힣]).{1,10}$', value):
        raise ValidationError(
            '닉네임은 2자 이상 10자 이하, 영어 또는 숫자 또는 한글로만 구성',
            params={'value': value},
        )


def validate_phone(value):
    if not re.match(r'^[0-9]{3}[0-9]{4}[0-9]{4}', value):
        raise ValidationError(
            '-없이 11자리 숫자 입력',
            params={'value': value},
        )


def validate_birth(value):
    None

