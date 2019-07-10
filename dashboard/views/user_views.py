import random
import string

from django.contrib.auth import authenticate
from django.shortcuts import redirect, render, reverse

from dashboard.form import *
from dashboard.models import *


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "所有字段都必须填写!"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request)
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    request.session['is_login'] = True
                    request.session['username'] = username
                    return redirect('/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'dashboard/login.html', locals())
    login_form = UserForm()
    return render(request, 'dashboard/login.html', locals())


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


# @csrf_exempt
# def forget(request):
#     if request.method == "POST":
#         forget_form = ForgetForm(request.POST)
#         message = "Please check the form."
#         print(forget_form)
#         if forget_form.is_valid():
#             email = forget_form.cleaned_data['email']
#             password1 = forget_form.cleaned_data['password1']
#             password2 = forget_form.cleaned_data['password2']
#             check_num = forget_form.cleaned_data['check']
#             print(check_num)
#             print(Check.objects.get(email=email).check)
#             if password1 != password2:  # 判断两次密码是否相同
#                 message = "两次输入的密码不同！"
#                 return render(request, 'dashboard/forget.html', locals())
#             elif not Check.objects.filter(email=email):
#                 message = "验证码未发送"
#                 return render(request, 'dashboard/forget.html', locals())
#             elif check_num != Check.objects.get(email=email).check:
#                 message = "验证码错误"
#                 return render(request, 'dashboard/forget.html', locals())
#             elif check_num == Check.objects.get(email=email).check:
#                 message = "修改成功"
#                 user = User.objects.get(email=email)
#                 user.set_password(password1)
#                 user.save()
#                 Check.objects.get(email=email).delete()
#                 return render(request, 'dashboard/forget.html', locals())
#     forget_form = ForgetForm()
#     return render(request, 'dashboard/forget.html', locals())


# def send(request):
#     try:
#         same_email = Check.objects.get(email=request.GET['email'])
#     except Check.DoesNotExist:
#         same_email = None
#     check_num = random_str(8)
#     if same_email:
#         same_email.check = check_num
#         same_email.save()
#     else:
#         temp = Check.objects.create(email=request.GET['email'], check=check_num)
#         temp.save()
#     res = send_mail('【Thu-dashboard修改密码】',
#                     '请在修改密码页面输入以下验证码：' + check_num,
#                     'thu_dashboard@sina.com',
#                     [request.GET['email']])
#     return HttpResponse(res)


# def logout(request):
#     if not request.session.get('is_login', None):
#         return redirect('/')
#     request.session.flush()
#     return redirect('/')


def random_str(n, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(n))

# def generate_token():
#     ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
#     return ran_str
#
#
# def generate_check():
#     ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
#     return ran_str
