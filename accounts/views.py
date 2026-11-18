from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import UserRegistrationForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.role == User.Role.ADMIN:
                return redirect('admin_dashboard')

            return redirect('reader_dashboard')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def reader_dashboard(request):
    if request.user.role != User.Role.READER:
        return HttpResponseForbidden('You are not allowed to access this page.')

    return render(request, 'accounts/reader_dashboard.html')


@login_required
def admin_dashboard(request):
    if request.user.role != User.Role.ADMIN:
        return HttpResponseForbidden('You are not allowed to access this page.')

    return render(request, 'accounts/admin_dashboard.html')


def user_logout(request):
    if request.method == 'POST':
        logout(request)

    return redirect('login')