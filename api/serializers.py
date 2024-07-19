from rest_framework import serializers
from web.models import Upload

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'

