from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


# Register your models here.
class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'nickname', 'gender', 'phone', 'birth', 'user_type', 'refresh_token', )}),
        ('Permissions', {'fields': ('is_admin', 'is_member', 'is_active', )}),
        ('Date info', {'fields': ('last_login', )})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'nickname', 'password1', 'password2')}
         ),
    )

    form = UserChangeForm
    add_from = UserCreationForm

    list_display = ('username', 'nickname', 'user_type')
    list_filter = ('is_admin',)
    search_fields = ('username', 'nickname')
    ordering = ('username',)

    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)