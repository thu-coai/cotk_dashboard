import random
import string

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse

from dashboard.form import *
from dashboard.models import *


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "Please check the form."
        if register_form.is_valid():
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

                return redirect(reverse('login'))
    register_form = RegisterForm()
    return render(request, 'dashboard/register.html', locals())


@login_required
def profile(request):
    print(request.user.profile.token)
    return render(request, 'dashboard/profile.html', locals())


def random_str(n, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(n))