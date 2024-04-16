from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User, Member


# Register your models here.
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None,          {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', )}),
        ('Date info',   {'fields': ('last_login', 'created_at', )}),
        ('Auth info',   {'fields': ('refresh_token', )})
    )

    readonly_fields = ['created_at', ]

    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('username', 'password1', 'password2')}
        ),
    )

    form = UserChangeForm
    add_from = UserCreationForm

    list_display = ('username',)
    list_filter = ('is_admin',)
    search_fields = ('username',)
    ordering = ('username',)

    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


class MemberAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'gender', 'birth', 'email']
    list_display = ('user', 'name', 'gender', 'birth', 'email')


admin.site.register(Member, MemberAdmin)
