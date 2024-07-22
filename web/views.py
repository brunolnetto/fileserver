# views.py
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import os

from .forms import UploadForm
from .models import Upload

def home_view(request):
    return render(request, 'web/home.html')

def handle_uploaded_file(f):
    # Save the file
    file_path = os.path.join('uploads', f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path

def validate_file_type(filename):
    valid_extensions = ['.csv', '.xlsx', '.xls']
    ext = os.path.splitext(filename)[1].lower()
    return ext in valid_extensions

@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        
        if not files:
            print('No files uploaded.')
            return JsonResponse({'status': 'error', 'message': 'No files uploaded'}, status=400)

        # Iterate over each file and process it
        for file in files:
            # Validate file type
            if not validate_file_type(file.name):
                return JsonResponse({'status': 'error', 'message': f'Invalid file type: {file.name}'}, status=400)

            # Save the file (assuming Upload model has a `file` field)
            upload = Upload(file=file)
            upload.save()

        print('Files uploaded successfully.')
        return JsonResponse({'status': 'success'})

    # Render the upload page for GET request
    return render(request, 'web/upload.html')

@csrf_exempt
def update_uploads(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            updates = data.get('updates', [])

            for item in updates:
                upload_id = item.get('id')
                file = item.get('file')
                filesize_kb = item.get('filesize_kb')

                if not all([upload_id, file, filesize_kb is not None]):
                    return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)

                upload = Upload.objects.get(id=upload_id)
                upload.file = file
                upload.filesize_kb = filesize_kb
                upload.save()

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Upload.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Upload not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

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

def custom_bad_request(request, exception=None):
    return render(request, 'web/status_code/400.html', status=400)

def custom_permission_denied(request, exception=None):
    return render(request, 'web/status_code/403.html', status=403)

def custom_page_not_found(request, exception=None):
    return render(request, 'web/status_code/404.html', status=404)

def custom_server_error(request):
    return render(request, 'web/status_code/500.html', status=500)

