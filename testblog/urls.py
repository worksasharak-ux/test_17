from django.urls import path
from .views import *

urlpatterns = [
    path('', main),
    path('user/<int:userid>', user_posts)
]