from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User

GENDER = {
        ("M", "Man"),
        ("W", "Woman"),
    }

REGION = {
    ("SEO", "서울특별시"),
    ("SEJ", "세종특별자치시"),
    ("BSN", "부산광역시"),
    ("DGU", "대구광역시"),
    ("ICN", "인천광역시"),
    ("GJU", "광주광역시"),
    ("DJN", "대전광역시"),
    ("USN", "울산광역시"),
    ("GNG", "경기도"),
    ("GWN", "강원특별자치도"),
    ("JBK", "전북특별자치도"),
    ("JJU", "제주특별자치도"),
    ("CBK", "충청북도"),
    ("CNM", "충청남도"),
    ("JNM", "전라남도"),
    ("GBK", "경상북도"),
    ("GNM", "경상남도"),
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
    region = models.CharField(_("region"), max_length=10, choices=REGION, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = "요양등급세부평가"
        verbose_name_plural = "요양등급세부평가 그룹"

    def set_user(self, user):
        self.user = user

    def set_gender(self, gender):
        self.gender = gender

    def set_age(self, age):
        self.age = age


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
    region = models.CharField(_("region"), max_length=10, choices=REGION, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = "요양등급간소평가"
        verbose_name_plural = "요양등급간소평가 그룹"


class CareGradeEx(models.Model):
    data = models.JSONField(_("data"))
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER)
    age = models.IntegerField(_("age"))
    region = models.CharField(_("region"), max_length=10, choices=REGION, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "비회원 요양등급평가"
        verbose_name_plural = "비회원 요양등급평가그룹"
