from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

import json

from .models import Record
from .form import UploadForm

# Create your views here.

def index(request):
	return HttpResponse("Under construction.")

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
