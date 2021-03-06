from django.shortcuts import render

from .users import register, profile_view, regenerate_token
from .records import upload, get, show, update, edit
from .table import RecordsJson, records


def index(request):
    user = request.user
    token = ""
    if user.is_authenticated:
        token = user.first_name
    #print('user={}'.format(user))
    #print('token={}'.format(token))
    return render(request, 'dashboard/index.html', locals())
