from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Post, Comment, PostLike

User = get_user_model()
# Create your views here.
def main(request):
    context = {
        "posts" : Post.objects.all(),
    }
    return render(request, 'main.html', context)

def user_posts(request,userid):

    context = {
        "posts" : Post.objects.filter(author_id=userid),
        "title" : User.objects.get(id=userid).username,
    }
    return render(request, 'main.html', context)

def view_post(request,postid):
    posts = Post.objects.filter(pk=postid)
    post = posts.first()
    context = {
        "post" : post,
        "comments" : Comment.objects.filter(post=post).order_by("-pk"),
        "user_liked": PostLike.objects.filter(post=post,author=request.user).exists()
    }
    return render(request, 'post.html', context)

def post_likes(request, postid): # лайкать посты
    posts = Post.objects.filter(pk=postid)
    post = posts.first() if posts else None
    referer = request.META.get("HTTP_REFERER")
    if post:
        likes = PostLike.objects.filter(post=post, author=request.user)
        if likes:
            likes.first().delete()
        else:
            PostLike.objects.create(
                post=post,
                author=request.user
            )
    return redirect(referer)

def post_comment(request, postid): # метод создания коммента
    posts = Post.objects.filter(pk=postid)
    post = posts.first() if posts else None
    if post:
        Comment.objects.create(
            post=post,
            author=request.user,
            text=request.POST.get("text")
        )
    return redirect(f"/post/{postid}")

@login_required # декоратор проверки авторизирован ли пользователь
def create_posts(request): # метод создания поста
    if request.method == 'POST':
        text = request.POST.get("post_text")
        if text:
            Post.objects.create(post_text=text, author=request.user) # добавление поста в базу(модели)
            return redirect("/")
        return render(request, "create_post.html", context={"error": 'Заполните поле!'})
    return render(request, 'create_post.html', )

