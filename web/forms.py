from django.forms import ModelForm
from .models import Upload

class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ['file']

