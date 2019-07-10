from django.shortcuts import render

from .user_views import login, register
from .record_views import upload, get, show


def index(request):
    user = request.user
    token = ""
    if user.is_authenticated:
        token = user.first_name
    print('user={}'.format(user))
    print('token={}'.format(token))
    return render(request, 'dashboard/index.html', locals())
