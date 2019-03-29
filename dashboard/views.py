from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives

import json
from .models import Record,Check
from .form import UploadForm,UserForm,RegisterForm,ForgetForm
import random
import string
# Create your views here.

def index(request):
	return render(request,'dashboard/index.html')

def login(request):
	if request.session.get('is_login', None):
		return redirect('/')
	if request.method == "POST":
		login_form = UserForm(request.POST)
		message = "所有字段都必须填写!"
		if login_form.is_valid():
			username = login_form.cleaned_data['username']
			password = login_form.cleaned_data['password']
			try:
				user = User.objects.get(username=username)
				if user.check_password(password):
					request.session['is_login']=True
					request.session['username']=username
					return redirect('/')
				else:
					message = "密码不正确！"
			except:
				message = "用户名不存在！"
		return render(request, 'dashboard/login.html',locals())
	login_form = UserForm()
	return render(request, 'dashboard/login.html',locals())


def register(request):
	if request.method=="POST":
		register_form = RegisterForm(request.POST)
		message="请检查填写内容"
		if register_form.is_valid():
			username = register_form.cleaned_data['username']
			password1 = register_form.cleaned_data['password1']
			password2 = register_form.cleaned_data['password2']
			email = register_form.cleaned_data['email']
			if password1 != password2:  # 判断两次密码是否相同
				message = "两次输入的密码不同！"
				return render(request, 'dashboard/register.html', locals())
			else:
				same_username = User.objects.filter(username=username)
				if same_username:
					message="用户名已存在！"
					return render(request,'dashboard/register.html',locals())
				same_email = User.objects.filter(email=email)
				if same_email:
					message="邮箱已被注册!"
					return render(request,'dashboard/register.html',locals())
				user = User.objects.create_user(username=username, email=email, password=password1,first_name=generate_token())
				return redirect('/login')
	register_form = RegisterForm()
	return render(request, 'dashboard/register.html',locals())

@csrf_exempt
def forget(request):
	if request.method=="POST":
		forget_form = ForgetForm(request.POST)
		message="请检查填写内容完整性"
		print(forget_form)
		if forget_form.is_valid():
			email = forget_form.cleaned_data['email']
			password1 = forget_form.cleaned_data['password1']
			password2 = forget_form.cleaned_data['password2']
			check_num = forget_form.cleaned_data['check']
			print(check_num)
			print(Check.objects.get(email=email).check)
			if password1 != password2:  # 判断两次密码是否相同
				message = "两次输入的密码不同！"
				return render(request, 'dashboard/forget.html', locals())
			elif not Check.objects.filter(email=email):
				message = "验证码未发送"
				return render(request, 'dashboard/forget.html', locals())
			elif check_num!=Check.objects.get(email=email).check:
				message = "验证码错误"
				return render(request, 'dashboard/forget.html', locals())
			elif check_num == Check.objects.get(email=email).check:
				message = "修改成功"
				user = User.objects.get(email=email)
				user.set_password(password1)
				user.save()
				Check.objects.get(email=email).delete()
				return render(request, 'dashboard/forget.html', locals())
	forget_form = ForgetForm()
	return render(request,'dashboard/forget.html',locals())

def send(request):
	same_email =  Check.objects.get(email=request.GET['email'])
	check_num = generate_check()
	if (same_email):
		same_email.check = check_num
		same_email.save()
	else:
		temp = Check.objects.create(email=request.GET['email'],check=check_num)
		temp.save()
	res = send_mail('【Thu-dashboard修改密码】',
					'请在修改密码页面输入以下验证码：'+check_num,
					'thu_dashboard@sina.com',
					[request.GET['email']])
	return HttpResponse(res)

def logout(request):
	if not request.session.get('is_login', None):
		return redirect('/')
	request.session.flush()
	return redirect('/')

@csrf_exempt
def upload(request):
	if request.method == "GET":
		return HttpResponseNotFound()

	form = UploadForm(request.POST)
	if not form.is_valid():
		print(form.errors.as_json())
		return HttpResponseBadRequest(json.dumps({"code": "bad", "err": form.errors.as_json()}))

	r = Record()
	r.git_user = form.cleaned_data['git_user']
	r.git_repo = form.cleaned_data['git_repo']
	r.git_commit = form.cleaned_data['git_commit']
	r.result = form.cleaned_data['result']
	r.other_config = {
		"entry": form.cleaned_data['entry'],
		"args": form.cleaned_data['args'],
		"working_dir": form.cleaned_data['working_dir'],
		"record_information": form.cleaned_data['record_information']
	}
	r.save()
	return HttpResponse(json.dumps({"code": "ok", "id": r.id}))

def show(request):
	if "id" not in request.GET:
		return HttpResponseBadRequest("ID not existed")
	try:
		r = Record.objects.get(id=request.GET["id"])
	except ObjectDoesNotExist as err:
		return HttpResponseBadRequest("ID not existed")

	res = {
		"git_user": r.git_user,
		"git_repo": r.git_repo,
		"git_commit": r.git_commit,
		"result": r.result,
		"other_config": r.other_config
	}
	return HttpResponse(json.dumps(res))

def generate_token():
	ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
	return ran_str

def generate_check():
	ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
	return ran_str
