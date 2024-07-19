from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .forms import UploadForm
from .models import Upload

def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UploadForm()
    return render(request, 'web/upload.html', {'form': form})

def upload_success(request):
    return render(request, 'web/success.html')

def upload_status(request):
    uploads_list = Upload.objects.all()
    paginator = Paginator(uploads_list, 10)  # Show 10 uploads per page

    page_number = request.GET.get('page')
    uploads = paginator.get_page(page_number)

    return render(request, 'web/status.html', {'uploads': uploads})