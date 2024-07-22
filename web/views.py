# views.py
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse

from .forms import UploadForm
from .models import Upload

def home_view(request):
    return render(request, 'web/home.html')

@csrf_protect
def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')
    else:
        form = UploadForm()
    return render(request, 'web/upload.html', {'form': form})

@csrf_protect
def delete_selected_uploads(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        file_ids = data.get('ids', [])
        if not isinstance(file_ids, list):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
        deleted_count = Upload.objects.filter(id__in=file_ids).delete()[0]
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