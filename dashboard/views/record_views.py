import json

from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from dashboard.form import UploadForm
from dashboard.models import *


@csrf_exempt
def upload(request):
    if request.method == "GET":
        return HttpResponseNotFound()

    try:
        print(request.POST)
        token = request.POST['token']
        form = request.POST['data']
        form = json.loads(form)
        form = UploadForm(form)
    except Exception as e:
        return HttpResponseBadRequest(json.dumps({"code": "wrong format", "err": str(e)}))

    try:
        user = User.objects.get(profile__token=token)
    except User.DoesNotExist as e:
        return HttpResponseBadRequest(json.dumps({"code": "bad token", "err": "token does not exist"}))

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
    return HttpResponse(json.dumps({"code": "ok", "id": user.id}))


def get(request):
    print(request.GET)
    if "id" not in request.GET:
        return HttpResponseBadRequest("ID not existed")
    try:
        r = Record.objects.get(id=request.GET["id"])
    except Record.DoesNotExist as e:
        return HttpResponseBadRequest("ID not existed")

    res = {
        "git_user": r.git_user,
        "git_repo": r.git_repo,
        "git_commit": r.git_commit,
        "result": r.result,
        "other_config": r.other_config
    }
    return HttpResponse(json.dumps(res))


def show(request):
    if request.user.is_authenticated:
        # return HttpResponse(json.dumps(
        #     {"total": 2, "rows": [{"id": 1, "git_user": "qsz", "git_repo": "repo_0", "git_commit": "commit_0",
        #                            "result": "result0", "other_config": {"key1": "item1", "key2": "item2"}},
        #
        #                           {"id": 2, "git_user": "wjq", "git_repo": "repo_2", "git_commit": "commit_2",
        #                            "result": "result2", "other_config": {"key1": "item1", "key2": "item2"}}]}))
        rows = []
        for i in range(10):
            try:
                record = Record.objects.get(id=i)
            except Record.DoesNotExist:
                pass
            else:
                rows.append({
                    'id': i,
                    'git_user': record.git_user,
                    'git_repo': record.git_repo,
                    'git_commit': record.git_commit,
                    'result': record.result,
                    'other_config': record.other_config
                })

        res = {
            "total": len(rows),
            "rows": rows
        }
        res = json.dumps(res)
        return HttpResponse(res)
    else:
        return redirect('/login')