from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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

@login_required # декоратор проверки авторизирован ли пользователь
def create_posts(request): # метод создания поста
    if request.method == 'POST':
        text = request.POST.get("post_text")
        if text:
            Post.objects.create(post_text=text, author=request.user) # добавление поста в базу(модели)
            return redirect("/")
        return render(request, "create_post.html", context={"error": 'Заполните поле!'})
    return render(request, 'create_post.html', )