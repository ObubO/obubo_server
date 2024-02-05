from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User

GENDER = {
        ("M", "Man"),
        ("W", "Woman"),
    }


# Create your models here.
class CareGrade(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    data = models.JSONField(_("data"), default=dict)
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER)
    age = models.IntegerField(_("age"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = "요양등급"
        verbose_name_plural = "요양등급 그룹"
