from django.contrib import admin

from .models import CareGrade


class CareGradeAdmin(admin.ModelAdmin):
    fields = ['user', 'age', 'gender', 'data', ]

    list_display = ('user', 'age', 'gender')


admin.site.register(CareGrade, CareGradeAdmin)
