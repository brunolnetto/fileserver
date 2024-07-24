from django.db.models import (
    CASCADE, ForeignKey, OneToOneField, BooleanField, OneToOneField, 
    Model, FileField, DateTimeField, CharField, IntegerField
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
import os

class UserProfile(Model):
    uspr_user = OneToOneField(User, on_delete=CASCADE)
    uspr_first_login = BooleanField(default=True)  # Flag to track first login

    def __str__(self):
        return self.user.username


class Upload(Model):
    uplo_user = ForeignKey(User, on_delete=CASCADE)
    uplo_file = FileField(upload_to='uploads/')
    uplo_uploaded_at = DateTimeField(auto_now_add=True)
    uplo_filename = CharField(max_length=255, blank=True)
    uplo_filesize = IntegerField(blank=True, null=True)
    uplo_description = CharField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        if self.uplo_file:
            self.filename = os.path.basename(self.uplo_file.name)
            self.filesize = self.uplo_file.size

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Upload")
        verbose_name_plural = _("Uploads")
        ordering = ['-uplo_uploaded_at']

    def __str__(self):
        return self.filename or str(self.uplo_file)
