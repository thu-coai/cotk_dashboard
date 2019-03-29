from django import forms
from django_mysql.forms import JSONField

class UploadForm(forms.Form):
    git_user = forms.CharField(max_length=50)
    git_repo = forms.CharField(max_length=50)
    git_commit = forms.CharField(max_length=40)
    entry = forms.CharField(max_length=50)
    args = JSONField(required=False)
    working_dir = forms.CharField(max_length=50)
    record_information = JSONField(required=False)
    result = JSONField()

class UserForm(forms.Form):
    username = forms.CharField(label="用户名",max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))

class ForgetForm(forms.Form):
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control','id':'email'}))
    check = forms.CharField(label="验证码",max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="新密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))