from django.contrib import admin

from .models import CareGradeEx, CareGradeSimple, CareGradeDetail


class CareGradeExAdmin(admin.ModelAdmin):
    fields = ['age', 'gender', 'data', 'region']
    list_display = ('age', 'gender', 'region')


class CareGradeSimpleAdmin(admin.ModelAdmin):
    fields = ['user', 'age', 'gender', 'data', 'region']
    list_display = ('user', 'age', 'gender', 'region')


class CareGradeDetailAdmin(admin.ModelAdmin):
    fields = ['user', 'age', 'gender', 'data', 'region']
    list_display = ('user', 'age', 'gender', 'region')


admin.site.register(CareGradeEx, CareGradeExAdmin)
admin.site.register(CareGradeSimple, CareGradeSimpleAdmin)
admin.site.register(CareGradeDetail, CareGradeDetailAdmin)
