from django.contrib import admin

from .models import *
# Register your models here.


class CommentsInLine(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','post_text', 'author', 'post_time','picture') # отображение постов

    list_editable = ('picture',) # что мы можем редактировать(картинки)

    readonly_fields = ('post_text', 'author', 'post_time')# поле для блокировки создания постов с админ панели

    search_fields = ('text', 'author__username') # поле поиска

    list_filter = ('author','post_time')

    fieldsets = ( #внутри поста меняет отображение
        ("Content", {"fields":("post_text","picture")}),
        ("Metadata", {"fields": ("author", "post_time")}),
    )
    inlines = [CommentsInLine]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','post', 'text', 'author', 'created_at','picture') # отображение коментариев

    list_editable = ('text',) # можем изменить текст

    readonly_fields = ('text', 'author', 'created_at')# поле для блокировки создания комментариев с админ панели

    search_fields = ('text', 'author__username') # поле поиска

    list_filter = ('author','created_at')

    fieldsets = (
        ("Content", {"fields": ("post", "text", "picture") }),
        ("Metadata", {"fields": ("author", "created_at") }),
    )

