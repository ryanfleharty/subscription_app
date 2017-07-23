# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.core.mail import send_mail
from .forms import RegisterForm, LoginForm
from social_django.models import UserSocialAuth

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.store_location = form.cleaned_data.get('store_location')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
        else:
            context = {
                'form' : form
            }
            return render(request, "users/register.html", context)
        return redirect('/')
    else:
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, "users/register.html", context)

@login_required
def profile(request):
    user = User.objects.get(id=request.user.id)
    subscriptions = user.profile.subscriptions.all()
    context = {
        'subscriptions': subscriptions
    }
    return render(request, "users/profile.html", context)

@login_required
def settings(request):
    user = request.user
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None
    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
    context = {
        'facebook_login' : facebook_login,
        'can_disconnect' : can_disconnect
    }
    return render(request, "users/settings.html", context)

@login_required
def set_password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:set_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'users/set_password.html', {'form': form})
