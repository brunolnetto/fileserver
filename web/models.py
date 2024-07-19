from django.db import models
from django.utils.translation import gettext_lazy as _
import os

class Upload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255, blank=True)
    filesize = models.IntegerField(blank=True, null=True)
    filetype = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.filename = os.path.basename(self.file.name)
            self.filesize = self.file.size
            self.filetype = self.file.content_type
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Upload")
        verbose_name_plural = _("Uploads")
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.filename or str(self.file)
