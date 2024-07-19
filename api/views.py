from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os
from django.core.files.storage import default_storage
from web.models import Upload
from .serializers import FileUploadSerializer

class FileUploadAPIView(APIView):
    def post(self, request):
        try:
            file = request.FILES['file']
            total_size = file.size
            uploaded_size = 0
            
            # Save file to MEDIA_URL
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file.name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                    uploaded_size += len(chunk)
                    progress = (uploaded_size / total_size) * 100

            # Save file information to the database
            Upload.objects.create(
                file='uploads/' + file.name,
                description=request.POST.get('description', '')
            )

            return Response({'status': 'file uploaded'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
