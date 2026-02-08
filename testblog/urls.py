from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', main),
    path('post/<int:postid>', view_post, name='post'),
    path('post/<int:postid>/like/', post_likes),
    path('post/<int:postid>/comment', post_comment),
    path('comments/<int:commentid>/clike/', comment_likes),
    path('user/<int:userid>', user_posts, name='posts_id'),
    path('user/<int:userid>/subscribe', subscribe, name='subscribe'),
    path('user/create-post', create_posts),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)