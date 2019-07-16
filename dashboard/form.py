from django import forms
from django_mysql.forms import JSONField


class UploadForm(forms.Form):
    entry = forms.CharField(max_length=100)
    args = JSONField(required=False)
    working_dir = forms.CharField(max_length=50, required=False)

    git_user = forms.CharField(max_length=50)
    git_repo = forms.CharField(max_length=50)
    git_commit = forms.CharField(max_length=40)

    record_information = JSONField(required=False)
    result = JSONField()


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=128, widget=forms.TextInput())
    password1 = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm Password", max_length=256, widget=forms.PasswordInput())
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput())

