from django.db.models import (
    OneToOneField, BooleanField, CASCADE,
    Model, FileField, DateTimeField, CharField, IntegerField
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import os

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_login = models.BooleanField(default=True)  # Flag to track first login

    def __str__(self):
        return self.user.username


class Upload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255, blank=True)
    filesize = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.filename = os.path.basename(self.file.name)
            self.filesize = self.file.size

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Upload")
        verbose_name_plural = _("Uploads")
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.filename or str(self.file)
