from django.contrib import admin

from .models import CareGradeEx, CareGradeSimple, CareGradeDetail


class CareGradeExAdmin(admin.ModelAdmin):
    fields = ['age', 'gender', 'data', ]
    list_display = ('age', 'gender')


class CareGradeSimpleAdmin(admin.ModelAdmin):
    fields = ['user', 'age', 'gender', 'data', ]
    list_display = ('user', 'age', 'gender')


class CareGradeDetailAdmin(admin.ModelAdmin):
    fields = ['user', 'age', 'gender', 'data', ]
    list_display = ('user', 'age', 'gender')


admin.site.register(CareGradeEx, CareGradeExAdmin)
admin.site.register(CareGradeSimple, CareGradeSimpleAdmin)
admin.site.register(CareGradeDetail, CareGradeDetailAdmin)
