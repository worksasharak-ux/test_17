from django.contrib import admin

from .models import *
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post_time','picture') # отображение постов

    readonly_fields = ('post_text', 'author', 'post_time')# поле для блокировки создания постов с админ панели

    search_fields = ('text', 'author__username') # поле поиска

    list_filter = ('author',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at','picture') # отображение постов

    readonly_fields = ('text', 'author', 'created_at')# поле для блокировки создания постов с админ панели

    search_fields = ('text', 'author__username') # поле поиска

    list_filter = ('author',)