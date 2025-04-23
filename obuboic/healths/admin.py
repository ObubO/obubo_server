from django.contrib import admin

from .models import CareGradeEx, CareGradeSimple, CareGradeDetail, GovService


@admin.register(CareGradeEx)
class CareGradeExAdmin(admin.ModelAdmin):
    list_display = (
        'gender', 'age', 'region', 'created_at'
    )
    list_filter = ('gender', 'region', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('기본 정보', {
            'fields': ('gender', 'age', 'region')
        }),
        ('등급 평가 데이터', {
            'fields': ('data',)
        }),
        ('시스템 정보', {
            'fields': ('created_at',)
        }),
    )


@admin.register(CareGradeSimple)
class CareGradeSimpleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'gender', 'age', 'region', 'created_at'
    )
    list_filter = ('gender', 'region', 'created_at')
    search_fields = ('user__id',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'gender', 'age', 'region')
        }),
        ('등급 평가 데이터', {
            'fields': ('data',)
        }),
        ('시스템 정보', {
            'fields': ('created_at',)
        }),
    )


@admin.register(CareGradeDetail)
class CareGradeDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'gender', 'age', 'region', 'created_at'
    )
    list_filter = ('gender', 'region', 'created_at')
    search_fields = ('user__id',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'gender', 'age', 'region')
        }),
        ('등급 평가 데이터', {
            'fields': ('data',)
        }),
        ('시스템 정보', {
            'fields': ('created_at',)
        }),
    )


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

