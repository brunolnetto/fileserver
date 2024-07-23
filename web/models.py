from django.db.models import (
    Model, FileField, DateTimeField, CharField, IntegerField
)

from django.utils.translation import gettext_lazy as _
import os

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
