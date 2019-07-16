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
    uploaded_at = models.DateTimeField(auto_now_add=True)

    entry = models.CharField(max_length=100)
    args = mysql_models.JSONField(null=True)
    working_dir = models.CharField(max_length=50, blank=True)

    git_user = models.CharField(max_length=50)
    git_repo = models.CharField(max_length=50)
    git_commit = models.CharField(max_length=40)

    record_information = mysql_models.JSONField(null=True)
    result = mysql_models.JSONField()

    def __str__(self):
        return self.git_str()

    def github_url(self):
        return 'https://github.com/{}/{}/commit/{}'.format(self.git_user, self.git_repo, self.git_commit)

    def git_str(self):
        return '{}/{}@{}'.format(self.git_user, self.git_repo, self.git_commit)


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
