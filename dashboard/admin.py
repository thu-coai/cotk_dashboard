from django.contrib import admin
from dashboard.models import Record, Dataloader, Profile

# Register your models here.

admin.site.register(Profile)
admin.site.register(Record)
admin.site.register(Dataloader)
