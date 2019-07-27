import random
import string

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseBadRequest

from dashboard.form import *
from dashboard.models import *


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "Invalid form."
        if not register_form.is_valid():
            return render(request, 'dashboard/register.html', locals())
        username = register_form.cleaned_data['username']
        password1 = register_form.cleaned_data['password1']
        password2 = register_form.cleaned_data['password2']
        email = register_form.cleaned_data['email']
        if password1 != password2:  # 判断两次密码是否相同
            message = "Passwords do not match."
            return render(request, 'dashboard/register.html', locals())
        else:
            same_username = User.objects.filter(username=username)
            if same_username:
                message = "Username already exists."
                return render(request, 'dashboard/register.html', locals())
            same_email = User.objects.filter(email=email)
            if same_email:
                message = "Email has been used"
                return render(request, 'dashboard/register.html', locals())

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            profile = Profile(
                user=user,
                token=random_str(16)
            )
            profile.save()

            return redirect('login')

    register_form = RegisterForm()
    return render(request, 'dashboard/register.html', locals())


@login_required
@require_POST
def regenerate_token(request):
    profile = request.user.profile

    new_token = random_str(16)
    while Profile.objects.filter(token=new_token).exists():
        new_token = random_str(16)
    profile.token = new_token
    profile.save()

    return redirect(profile_view)


@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)
        message = 'Invalid form.'
        if not profile_form.is_valid():
            return render(request, 'dashboard/profile.html', locals())
        data = profile_form.cleaned_data

        old_password = data['old_password']
        if not request.user.check_password(old_password):
            message = 'Old password wrong.'
            return render(request, 'dashboard/profile.html', locals())

        new_password = data['password1']
        if new_password:
            request.user.set_password(new_password)

        email = data['email']
        request.user.email = email
        request.user.save()

        return redirect('login')
    else:
        profile_form = UserProfileForm(initial={
            'email': request.user.email
        })
        return render(request, 'dashboard/profile.html', locals())


def random_str(n, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(n))
