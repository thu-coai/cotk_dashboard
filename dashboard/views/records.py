import json

from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from dashboard.form import UploadForm, RecordEditForm
from dashboard.models import *


@csrf_exempt
def upload(request):
    if request.method == 'GET':
        return HttpResponseNotFound()

    print('uploading...')
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
    rid = request.GET.get('rid', None)
    if not rid:
        raise Http404('ID does not exist')

    try:
        record = Record.objects.get(id=rid)
    except Record.DoesNotExist:
        raise Http404('ID does not exist')

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
    rid = request.GET.get('id', None)
    if not rid:
        raise Http404('ID does not exist')

    try:
        record = Record.objects.get(id=rid)
    except Record.DoesNotExist:
        raise Http404('ID does not exist')

    if record.hidden and record.user != request.user:
        raise Http404('Permission denied')

    config = {
        'entry': record.entry,
        'args': record.args,
        'working_dir': record.working_dir,
    }
    return render(request, 'dashboard/show.html', locals())


@login_required
def edit(request):
    if request.method == 'GET':
        rid = request.GET.get('id', None)
        if not rid:
            raise Http404('ID does not exist')
        try:
            record = Record.objects.get(id=rid)
        except Record.DoesNotExist:
            raise Http404('ID does not exist')
        if record.user != request.user:
            raise Http404('Permission denied')

        form = RecordEditForm(instance=record)
        return render(request, 'dashboard/edit.html', locals())
    elif request.method == 'POST':
        rid = request.POST.get('id', None)
        if not rid:
            return HttpResponseBadRequest('ID does not exist')
        try:
            record = Record.objects.get(id=rid)
        except Record.DoesNotExist:
            return HttpResponseBadRequest('ID does not exist')
        if record.user != request.user:
            return HttpResponseBadRequest('Permission denied')

        if 'delete' in request.POST:
            record.delete()
            return redirect('records')

        form = RecordEditForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('/show?id={}'.format(rid))
        else:
            return HttpResponseBadRequest('Invalid form')


@login_required
@require_POST
def update(request):
    rid = request.POST.get('id', None)
    if not rid:
        return HttpResponseBadRequest('ID does not exist')

    try:
        record = Record.objects.get(id=rid)
    except Record.DoesNotExist:
        return HttpResponseBadRequest('ID does not exist')

    if record.user != request.user:
        return HttpResponseBadRequest('You have no permission to do this')

    description = request.POST.get('description', None)
    if description:
        try:
            record.description = description
            record.save()
        except DatabaseError:
            return HttpResponseBadRequest('Description too long')
        return redirect('/show?id={}'.format(rid))

    # No content
    return HttpResponse(status=204)
