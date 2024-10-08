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
    uspr_first_login = BooleanField(default=True)

    def __str__(self):
        return self.uspr_user.username


class PendingRegistration(models.Model):
    pere_username = models.CharField(max_length=150, unique=True)
    pere_email = models.EmailField(unique=True)
    pere_hashed_password = models.CharField(max_length=128)
    pere_created_at = models.DateTimeField(auto_now_add=True)
    pere_activation_token = models.CharField(max_length=255)
    pere_is_activated = models.BooleanField(default=False)

class EmailQueue(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Upload(Model):
    uplo_user = ForeignKey(User, on_delete=CASCADE)
    uplo_file = FileField(upload_to='uploads/')
    uplo_uploaded_at = DateTimeField(auto_now_add=True)
    uplo_filename = CharField(max_length=255, blank=True)
    uplo_filesize = IntegerField(blank=True, null=True)
    uplo_description = CharField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        if self.uplo_file:
            self.uplo_filename = os.path.basename(self.uplo_file.name)
            self.uplo_filesize = self.uplo_file.size

        super().save(*args, **kwargs)

    @staticmethod
    def get_delete_field():
        return 'uplo_file'
    
    @staticmethod
    def get_visible_columns():
        return [
            'id',
            'uplo_file',
            'uplo_uploaded_at',
            'uplo_filename',
            'uplo_filesize',
            'uplo_description'
        ]
    
    @staticmethod
    def get_column_labels():
        """Returns a dictionary of column names and their labels."""
        return {
            'id': 'ID',
            'uplo_user': 'User',
            'uplo_file': 'File',
            'uplo_uploaded_at': 'Uploaded At',
            'uplo_filename': 'Filename (Bytes)',
            'uplo_filesize': 'Filesize',
            'uplo_description': 'Description'
        }

    @staticmethod
    def get_editable_columns():
        """Returns a list of fields that are editable."""
        return ['uplo_description']
    
    class Meta:
        verbose_name = _("Upload")
        verbose_name_plural = _("Uploads")
        ordering = ['-uplo_uploaded_at']

    def __str__(self):
        return self.uplo_filename or str(self.uplo_file)

