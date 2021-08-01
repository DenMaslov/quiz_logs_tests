from django.shortcuts import redirect, render
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout

import logging


log = logging.getLogger("auth_info")


def register(request):
    form = CreateUserForm()
    error = None
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            log.debug(f"Registered user {request.POST.get('username')}")
            form.save()
            return redirect("login")
        else:
            log.debug(f"Registration failed")
            error = "Invalid data, check the fields"

    context = {'form':form, 'error':error}
    return render(request, 'users/register.html', context)

def login_user(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            log.debug(f"Login user: {user.get_username()}")
            login(request, user)
            return redirect('tests_list')
    context = {}
    return render(request, 'users/login.html', context)

def logout_user(request):
    log.debug(f"Log out user: {request.user.username}")
    logout(request)
    return redirect('login')