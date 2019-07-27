from django import forms
from django_mysql.forms import JSONField
from dashboard.models import Record


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


class RecordEditForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['description', 'hidden']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10})
        }


class UserProfileForm(forms.Form):
    old_password = forms.CharField(label="Old Password", max_length=256, widget=forms.PasswordInput)
    password1 = forms.CharField(label="New Password (Leave blank to remain unchanged)", max_length=256,
                                widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirm New Password", max_length=256, widget=forms.PasswordInput,
                                required=False)
    email = forms.CharField(label="Email Address", max_length=256,
                            widget=forms.EmailInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError(
                'Passwords do not match.'
            )
