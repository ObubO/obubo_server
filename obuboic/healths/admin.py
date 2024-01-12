from django.contrib import admin

from .models import CareGrade


class CareGradeAdmin(admin.ModelAdmin):
    fields = ['user', 'birth', 'gender', 'data', ]


admin.site.register(CareGrade, CareGradeAdmin)
