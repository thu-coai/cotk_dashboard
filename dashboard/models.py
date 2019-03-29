from django.db import models

# Create your models here.

from django_mysql.models import JSONField

class Record(models.Model):
    git_user = models.CharField(max_length=50)
    git_repo = models.CharField(max_length=50)
    git_commit = models.CharField(max_length=40)
    result = JSONField()
    other_config = JSONField()

class Check(models.Model):
    email = models.EmailField(max_length=50)
    check = models.CharField(max_length=50)
    def __str__(self):
        return self.email