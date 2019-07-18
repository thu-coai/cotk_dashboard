import json

from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from dashboard.form import UploadForm
from dashboard.models import *


@csrf_exempt
def upload(request):
    if request.method == "GET":
        return HttpResponseNotFound()

    print(request.POST)

    try:
        form = request.POST['data']
        form = json.loads(form)
        form = UploadForm(form)
    except Exception as e:
        return HttpResponseBadRequest(json.dumps({
            "code": "wrong format",
            "err": str(e)
        }))

    try:
        token = request.POST['token']
        user = User.objects.get(profile__token=token)
    except User.DoesNotExist as e:
        return HttpResponseBadRequest(json.dumps({
            "code": "bad token",
            "err": "token does not exist",
        }))

    if not form.is_valid():
        print(form.errors.as_json())
        return HttpResponseBadRequest(json.dumps({
            "code": "invalid form",
            "err": form.errors.as_json(),
        }))

    record = Record(
        user=user,

        entry=form.cleaned_data['entry'],
        args=form.cleaned_data['args'],
        working_dir=form.cleaned_data['working_dir'],

        git_user=form.cleaned_data['git_user'],
        git_repo=form.cleaned_data['git_repo'],
        git_commit=form.cleaned_data['git_commit'],

        record_information=form.cleaned_data['record_information'],
        result=form.cleaned_data['result'],
    )

    record.save()

    return HttpResponse(json.dumps({
        "code": "ok",
        "id": record.id,
    }))


def get(request):
    print(request.GET)
    if 'id' not in request.GET:
        return HttpResponseBadRequest('ID does not exist')
    try:
        record = Record.objects.get(id=request.GET["id"])
    except Record.DoesNotExist as e:
        return HttpResponseBadRequest('ID does not exist')

    res = {
        'id': record.id,
        'user': record.user.username,

        'entry': record.entry,
        'args': record.args,
        'working_dir': record.working_dir,

        'git_user': record.git_user,
        'git_repo': record.git_repo,
        'git_commit': record.git_commit,

        'record_information': record.record_information,
        'result': record.result,
    }
    return HttpResponse(json.dumps(res))


def show(request):
    if 'id' not in request.GET:
        raise Http404('Wrong format')
    rid = request.GET['id']

    try:
        record = Record.objects.get(id=rid)
    except Record.DoesNotExist as e:
        raise Http404('ID not exists')

    config = {
        'entry': record.entry,
        'args': record.args,
        'working_dir': record.working_dir,
    }
    return render(request, 'dashboard/show.html', locals())
