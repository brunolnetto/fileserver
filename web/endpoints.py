import os
from django.conf import settings
from rest_framework.decorators import api_view
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Upload

# 1 MB chunks
CHUNKSIZE = 1024 * 1024



@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        try:
            file = request.FILES.get('file')
            if not file:
                return JsonResponse({'status': 'error', 'message': 'No file uploaded'}, status=400)

            total_size = file.size
            chunk_size = CHUNKSIZE
            uploaded_size = 0
            
            channel_layer = get_channel_layer()
            
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file.name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks(chunk_size):
                    destination.write(chunk)
                    uploaded_size += len(chunk)
                    progress = (uploaded_size / total_size) * 100
                    async_to_sync(channel_layer.group_send)(
                        'upload_progress',
                        {
                            'type': 'send_progress',
                            'progress': progress
                        }
                    )
            
            upload_instance = Upload(
                file='uploads/' + file.name,
                filename=file.name,
                filesize=file.size,
                filetype=file.content_type,
                description=request.POST.get('description', '')
            )
            upload_instance.save()
            
            return JsonResponse({'status': 'file uploaded'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@api_view(['GET'])
def upload_status(request):
    uploads = Upload.objects.all()
    return JsonResponse({'uploads': [upload.filename for upload in uploads]})
