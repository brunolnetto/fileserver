# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os
import uuid

from web.models import Upload

class FileUploadAPIView(APIView):
    def post(self, request):
        try:
            file = request.FILES['file']
            total_size = file.size
            uploaded_size = 0
            
            # Save file to MEDIA_URL
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Check if file with same name exists and generate a unique file name if necessary
            file_name, file_extension = os.path.splitext(file.name)
            unique_file_name = file.name
            counter = 1
            while os.path.exists(os.path.join(upload_dir, unique_file_name)):
                unique_file_name = f"{file_name}_{counter}{file_extension}"
                counter += 1
            
            file_path = os.path.join(upload_dir, unique_file_name)
            
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                    uploaded_size += len(chunk)
                    progress = (uploaded_size / total_size) * 100

            # Save file information to the database
            Upload.objects.create(
                file='uploads/' + unique_file_name,
                description=request.POST.get('description', '')
            )

            return Response({'status': 'file uploaded'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
