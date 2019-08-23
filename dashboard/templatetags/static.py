from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

class SettingsStaticRoot(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        prefix = request.META.get('SCRIPT_NAME')

        old_static_url = settings.STATIC_URL
        settings.STATIC_URL = prefix + old_static_url

        print("now use: " + settings.STATIC_URL)
        response = self.get_response(request)

        settings.STATIC_URL = old_static_url

        return response

@register.simple_tag
def static(value):
    return settings.STATIC_URL + value
