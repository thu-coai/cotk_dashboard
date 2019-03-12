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
