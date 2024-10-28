from django.contrib import admin

from .models import Posts


# Register your models here.
class PostsAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'content', 'created_at', 'updated_at']
    list_display = ('id', 'title', 'author', )

    readonly_fields = ['created_at', 'updated_at', ]

    search_fiedls = ('author', 'title')
    ordering = ('-created_at', )


admin.site.register(Posts, PostsAdmin)
