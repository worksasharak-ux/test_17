from django.contrib import admin

from .models import Post
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post_time') # отображение постов

    readonly_fields = ('post_text', 'author', 'post_time')# поле для блокировки создания постов с админ панели

    search_fields = ('text', 'author__username') # поле поиска

    list_filter = ('author',)