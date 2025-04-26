from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User, UserProfile, UserType, Terms, UserTerms


# Register your models here.
@admin.register(User)
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

    list_display = ('username', 'is_active')
    list_filter = ('is_admin', 'is_active')
    search_fields = ('username',)
    ordering = ('username',)

    filter_horizontal = ()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'nickname', 'gender', 'phone', 'birth', 'email', 'user_type', ]
    list_display = ('user', 'name', 'user_type', 'is_active')

    def is_active(self, obj):
        return obj.user.is_active

    search_fields = ('name', 'user_type')
    ordering = ('name',)


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    fields = ['id', 'name', ]
    list_display = ('id', 'name', )


@admin.register(Terms)
class TermsAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'is_necessary', ]
    list_display = ('title', 'is_necessary', )

    readonly_fields = []

    serach_fields = ('title', )
    ordering = ('title', )


@admin.register(UserTerms)
class UserTermsAdmin(admin.ModelAdmin):
    fields = ['user', 'terms', 'is_consent', 'consent_date', ]
    list_display = ('user', 'terms', 'is_consent', )

    readonly_fields = ['user', 'terms', 'is_consent', 'consent_date', ]

    search_fiedls = ('user',)
    ordering = ('user', )


admin.site.unregister(Group)
