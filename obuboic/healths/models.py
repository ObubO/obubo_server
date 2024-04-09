from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User

GENDER = {
        ("M", "Man"),
        ("W", "Woman"),
    }


# Create your models here.
class CareGradeDetail(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    data = models.JSONField(_("data"))
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER)
    age = models.IntegerField(_("age"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = "요양등급세부평가"
        verbose_name_plural = "요양등급세부평가 그룹"


class CareGradeSimple(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    data = models.JSONField(_("data"))
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER)
    age = models.IntegerField(_("age"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = "요양등급간소평가"
        verbose_name_plural = "요양등급간소평가 그룹"


class CareGradeEx(models.Model):
    data = models.JSONField(_("data"))
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER)
    age = models.IntegerField(_("age"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "비회원 요양등급평가"
        verbose_name_plural = "비회원 요양등급평가그룹"
