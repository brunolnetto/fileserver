from django.db.models import (
    OneToOneField, BooleanField, CASCADE,
    Model, FileField, DateTimeField, CharField, IntegerField
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
import os

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_login = models.BooleanField(default=True)  # Flag to track first login

    def __str__(self):
        return self.user.username


class Upload(Model):
    file = FileField(upload_to='uploads/')
    uploaded_at = DateTimeField(auto_now_add=True)
    filename = CharField(max_length=255, blank=True)
    filesize = IntegerField(blank=True, null=True)
    description = CharField(max_length=500, blank=True)

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
