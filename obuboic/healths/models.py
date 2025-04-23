from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User

GENDER = (
        ("M", "Man"),
        ("W", "Woman"),
)

REGION = (
    ("ALL", "전국"),
    ("SEO", "서울특별시"),
    ("SEJ", "세종특별자치시"),
    ("BSN", "부산광역시"),
    ("DGU", "대구광역시"),
    ("ICN", "인천광역시"),
    ("GJU", "광주광역시"),
    ("DJN", "대전광역시"),
    ("USN", "울산광역시"),
    ("경기도", "경기도"),
    ("GWN", "강원특별자치도"),
    ("JBK", "전북특별자치도"),
    ("JJU", "제주특별자치도"),
    ("CBK", "충청북도"),
    ("CNM", "충청남도"),
    ("JNM", "전라남도"),
    ("GBK", "경상북도"),
    ("GNM", "경상남도"),
)


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


class GovService(models.Model):
    service_id = models.CharField(verbose_name='서비스 ID', max_length=128)
    name = models.CharField(_("서비스명"), max_length=256)
    purpose = models.TextField(_("서비스 목적"))
    category = models.CharField(_("서비스 분야"), max_length=128)

    has_region = models.BooleanField(verbose_name='지역제한', default=False)
    region = models.CharField(verbose_name='지역명', max_length=128, null=True, blank=True)
    region_detail = models.CharField(verbose_name='지역 상세명', max_length=128, null=True, blank=True)
    deadline = models.DateField(verbose_name='마감기한', null=True, blank=True)

    organization_name = models.CharField(verbose_name='소관기관명', max_length=128)
    organization_phone = models.CharField(verbose_name='전화번호', max_length=128, null=True, blank=True)

    description = models.TextField(verbose_name='지원내용')
    target_audience = models.TextField(verbose_name='지원대상')
    age_limit = models.IntegerField(verbose_name='나이제한', null=True, blank=True)

    detail_url = models.URLField(verbose_name='상세조회URL', max_length=256, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 'gov_service'
        verbose_name = "정부 서비스"
        verbose_name_plural = "정부 서비스 목록"

    def __str__(self):
        return f"[{self.service_id}] {self.name}"
