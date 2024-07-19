from django.shortcuts import render, redirect
from .forms import UploadForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UploadForm()
    
    return render(request, 'fileuploader/upload.html', {'form': form})

def upload_success(request):
    return render(request, 'fileuploader/success.html')

