from django.urls import path
from .views import *

urlpatterns = [
    path('', main),
    path('post/<int:postid>', view_post, name='post'),
    path('post/<int:postid>/comment', post_comment),
    path('post/<int:postid>/like/', post_likes),
    path('comments/<int:commentid>/clike/', comment_likes), #test vesion
    path('user/<int:userid>', user_posts, name='posts_id'),
    path('user/create-post', create_posts),

]