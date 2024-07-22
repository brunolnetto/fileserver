# views.py
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import os

from .forms import UploadForm
from .models import Upload

def home_view(request):
    return render(request, 'web/home.html')

@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        if not files:
            print('No files uploaded.')
            return JsonResponse({'status': 'error', 'message': 'No files uploaded'}, status=400)

        for file in files:
            upload = Upload(file=file)
            upload.save()

        print('Files uploaded successfully.')
        return JsonResponse({'status': 'success'})

    # Render the upload page for GET request
    return render(request, 'web/upload.html')

@csrf_protect
def delete_selected_uploads(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        file_ids = data.get('ids', [])

        if not isinstance(file_ids, list):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

        uploads_to_delete = Upload.objects.filter(id__in=file_ids)
        deleted_count = uploads_to_delete.count()

        for upload in uploads_to_delete:
            file_path = os.path.join(settings.MEDIA_ROOT, upload.file.name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        uploads_to_delete.delete()

        return JsonResponse({'status': 'success', 'deleted_count': deleted_count})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def upload_success(request):
    return render(request, 'web/success.html')

def upload_status(request):
    uploads_list = Upload.objects.all()
    
    # Convert filesize from bytes to megabytes
    for upload in uploads_list:
        # Convert to MB
        upload.filesize_kb = upload.filesize / 1024
    
    # Show 10 uploads per page
    paginator = Paginator(uploads_list, 10)  

    page_number = request.GET.get('page')
    uploads = paginator.get_page(page_number)

    return render(request, 'web/status.html', {'uploads': uploads})