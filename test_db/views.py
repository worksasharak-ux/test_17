from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout

user_model = get_user_model()

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if  username == "":
            return redirect("/login")

        user = authenticate(username=username, password=password)
        if user is None:
            return redirect("/login")

        auth_login(request, user)
        return redirect("/posts")

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if  username == "":
            return redirect("/register")

        user_model.objects.create_user(
            username=username,
            password=password
        )
        user = authenticate(username=username, password=password)
        if user is None:
            return redirect("/register")

        auth_login(request, user)
        return redirect("/posts")


    return render(request,'register.html')

def logout(request):
    auth_logout(request)
    return redirect("/login")
