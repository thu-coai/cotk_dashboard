from django.conf import settings

class SettingsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        prefix = request.META.get('SCRIPT_NAME')
        old_static_url = settings.STATIC_URL
        settings.STATIC_URL = prefix + old_static_url

        response = self.get_response(request)

        settings.STATIC_URL = old_static_url

        return response
