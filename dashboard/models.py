from django.utils import timezone

from django.db import models

import django_mysql.models as mysql_models
from django.contrib.auth.models import User


class Record(models.Model):
    """
    Uploaded Record
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    uploaded_at = models.DateTimeField(default=timezone.now)

    entry = models.CharField(max_length=100, blank=True)
    args = mysql_models.JSONField(null=True, blank=True)
    working_dir = models.CharField(max_length=50, blank=True)

    git_user = models.CharField(max_length=50)
    git_repo = models.CharField(max_length=50)
    git_commit = models.CharField(max_length=40)

    record_information = mysql_models.JSONField(null=True, blank=True)

    result = mysql_models.JSONField()

    description = models.CharField(max_length=1000, blank=True)

    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.github_str

    @property
    def github_url(self):
        return 'https://github.com/{}/{}/tree/{}'.format(self.git_user, self.git_repo, self.git_commit)

    @property
    def github_str(self):
        return '{}/{}@{}'.format(self.git_user, self.git_repo, self.git_commit[:6])


class Dataloader(models.Model):
    file_id = models.CharField(max_length=100)

    clsname = models.CharField(max_length=100)

    record = models.ForeignKey(
        Record,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '{} ({})'.format(self.clsname, self.file_id)


class Profile(models.Model):
    """
    User profile
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    token = models.CharField(max_length=50)

    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.token)
