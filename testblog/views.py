from platform import freedesktop_os_release
from sys import is_stack_trampoline_active

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ViewDoesNotExist
from django.shortcuts import render, redirect
from .models import *

user = get_user_model()
# Create your views here.
def main(request):
    all_subscriptions = (
        Subscription.objects.filter(follower=request.user))
    unviewed_posts = []
    for subs in all_subscriptions:
        subs_posts = Post.objects.filter(author=subs.page_user)
        for sub_post in subs_posts:
            if not Views.objects.filter(post=sub_post,
                                        follower=request.user).exists():
                unviewed_posts.append(sub_post)

    context = {
        "posts" : Post.objects.all().order_by('-post_time'),
        "unviewed_posts": unviewed_posts
    }
    return render(request, 'main.html', context)

def user_posts(request,userid):
    subscription = Subscription.objects.filter(page_user_id=userid, follower=request.user)
    context = {
        "posts" : Post.objects.filter(author_id=userid),
        "user_page" : user.objects.get(id=userid),
        "subscribed": subscription,
    }
    return render(request, 'main.html', context)

def subscribe(request,userid):

    page_user = user.objects.filter(pk=userid)
    if not page_user:
        return redirect("/")
    referer = request.META.get("HTTP_REFERER")
    page_user = page_user.first()
    active_subscription = Subscription.objects.filter(page_user=page_user, follower=request.user)
    if active_subscription:
        active_subscription.delete()
    else:
        Subscription.objects.create(page_user=page_user, follower=request.user)

    return redirect(referer)

def view_post(request,postid):#просмотр постов
    posts = Post.objects.filter(pk=postid)
    post = posts.first()

    if request.user.is_authenticated: #просмотр новых записей
        Views.objects.get_or_create(post=post, follower=request.user)

    context = {
        "post" : post,
        "comments" : Comment.objects.filter(post=post).order_by("-pk"),
        "user_liked": PostLike.objects.filter(post=post,author=request.user).exists()
    }
    return render(request, 'post.html', context)

@login_required # декоратор проверки авторизирован ли пользователь
def create_posts(request): # метод создания поста
    if request.method == 'POST':
        text = request.POST.get("post_text")
        picture = request.FILES.get("picture")
        if text or picture:
            Post.objects.create(post_text=text,
                                author=request.user,
                                picture=picture) # добавление поста в базу(модели)
            return redirect("/")
        return render(request, "create_post.html", context={"error": 'Заполните поле!'})
    return render(request, 'create_post.html', )

@login_required
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

@login_required
def post_comment(request, postid): # метод создания коммента
    if request.method == "POST":
        posts = Post.objects.filter(pk=postid)
        text = request.POST.get("text")
        picture = request.FILES.get("picture")
        post = posts.first() if posts else None
        if post:
            if text or picture:
                Comment.objects.create(
                    post=post,
                    author=request.user,
                    text=text,
                    picture=picture,
                )
        return redirect(f"/post/{postid}")

@login_required
def comment_likes(request, commentid): # лайкать посты
    comments = Comment.objects.filter(pk=commentid)
    comment = comments.first() if comments else None
    referer = request.META.get("HTTP_REFERER")
    if comment:
        likes = CommentLike.objects.filter(comment=comment, author=request.user)
        if likes:
            likes.first().delete()
        else:
            CommentLike.objects.create(
                comment=comment,
                author=request.user
            )
    return redirect(referer)