from django.contrib import admin

from .models import CareGradeEx, CareGradeSimple, CareGradeDetail, GovService


class CareGradeExAdmin(admin.ModelAdmin):
    fields = ['age', 'gender', 'data', 'region']
    list_display = ('age', 'gender', 'region')


class CareGradeSimpleAdmin(admin.ModelAdmin):
    fields = ['user', 'age', 'gender', 'data', 'region']
    list_display = ('user', 'age', 'gender', 'region')


class CareGradeDetailAdmin(admin.ModelAdmin):
    fields = ['user', 'age', 'gender', 'data', 'region']
    list_display = ('user', 'age', 'gender', 'region')


@admin.register(GovService)
class GovServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category',
        'region', 'deadline',
        'organization_name', 'created_at', 'updated_at'
    )
    list_filter = ('category', 'region', 'deadline', 'created_at')
    search_fields = ('service_id', 'name', 'organization_name', 'region')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('기본 정보', {
            'fields': ('service_id', 'name', 'purpose', 'category')
        }),
        ('지역 정보', {
            'fields': ('has_region', 'region', 'region_detail')
        }),
        ('기관 정보', {
            'fields': ('organization_name', 'organization_phone')
        }),
        ('지원 정보', {
            'fields': ('description', 'target_audience', 'age_limit', 'deadline', 'detail_url')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at')
        }),
    )


admin.site.register(CareGradeEx, CareGradeExAdmin)
admin.site.register(CareGradeSimple, CareGradeSimpleAdmin)
admin.site.register(CareGradeDetail, CareGradeDetailAdmin)
