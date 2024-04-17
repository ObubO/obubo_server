from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User, Member, UserType, TAC, TACAgree


# Register your models here.
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None,          {'fields': ('username', 'password')}),
        ('날짜정보',      {'fields': ('last_login', 'created_at', 'updated_at', )}),
        ('활성여부',      {'fields': ('is_active',)}),
    )

    readonly_fields = ['created_at', 'updated_at', 'last_login', ]

    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('username', 'password1', 'password2')}),
    )

    form = UserChangeForm
    add_from = UserCreationForm

    list_display = ('username',)
    list_filter = ('is_admin',)
    search_fields = ('username',)
    ordering = ('username',)

    filter_horizontal = ()


class MemberAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'gender', 'phone', 'birth', 'email', 'user_type', ]
    list_display = ('user', 'name', 'gender', )

    search_fields = ('name',)
    ordering = ('name',)


class UserTypeAdmin(admin.ModelAdmin):
    fields = ['type_name', ]
    list_display = ('type_name', )


class TACAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'is_necessary', ]
    list_display = ('title', )

    readonly_fields = ['title', 'content', 'is_necessary', ]


class TACAgreeAdmin(admin.ModelAdmin):
    fields = ['user', 'tac', 'is_consent', 'consent_date', ]
    list_display = ('user', 'tac', 'is_consent', )

    readonly_fields = ['user', 'tac', 'is_consent', 'consent_date', ]

    search_fields = ('user',)
    ordering = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(UserType, UserTypeAdmin)
admin.site.register(TAC, TACAdmin)
admin.site.register(TACAgree, TACAgreeAdmin)
admin.site.unregister(Group)
