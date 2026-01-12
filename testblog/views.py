from django.shortcuts import render
from .models import  Post

# Create your views here.
def main(request):
    context = {
        "posts" : Post.objects.all(),
    }
    return render(request, 'main.html', context)

def user_posts(request,userid):
    context = {
        "posts" : Post.objects.filter(author_id=userid),
    }
    return render(request, 'main.html', context)