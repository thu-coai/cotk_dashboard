from django.db import models

from django_mysql.models import JSONField
from django.contrib.auth.models import User


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


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    token = models.CharField(max_length=50)
