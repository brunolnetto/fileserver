# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.conf import settings
import json
import os

from .utils import custom_error_reponse
from .forms import UploadForm
from .models import Upload

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetView

from .forms import CustomPasswordResetForm

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset_form.html'

def home_view(request):
    return render(request, 'web/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page or a dashboard
        else:
            # Handle invalid login
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def login_required_view(request):
    return render(request, 'registration/login_required.html')

@csrf_exempt
def check_username(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username', '')
            exists = User.objects.filter(username=username).exists()
            return JsonResponse({'exists': exists})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def send_test_email(request):
    send_mail(
        'Test Email Subject',
        'This is a test email message.',
        settings.EMAIL_HOST_USER,
        ['recipient@example.com'],
        fail_silently=False,
    )
    return HttpResponse("Test email sent!")

@require_POST
def check_email(request):
    email = request.POST.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})

@login_required
@csrf_exempt
def update_first_login_flag(request):
    if request.method == 'POST':
        user_profile = request.user.userprofile
        if user_profile.first_login:
            user_profile.first_login = False
            user_profile.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'registration/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'registration/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'registration/signup.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, 'Sign up successful.')
        return redirect('home')  # Redirect to home or another page

    return render(request, 'registration/signup.html')

@login_required
@login_required
def settings_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Update the user profile, excluding username
        user = request.user
        user.email = email
        user.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('settings')  # Redirect back to the settings page

    return render(request, 'web/settings.html')


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
@login_required
def upload_files_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        
        if not files:
            return custom_error_reponse('No files uploaded', 400)
        
        # Get the current user
        user = request.user
        
        # Iterate over each file and process it
        for file in files:
            # Validate file type
            if not validate_file_type(file.name):
                return custom_error_reponse(f'Invalid file type: {file.name}', status=400)

            # Save the file (assuming Upload model has a `file` field)
            upload = Upload(file=file, user_id=user)
            upload.save()

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
                    return custom_error_reponse('Missing data', 400)

                upload = Upload.objects.get(id=upload_id)
                upload.file = file
                upload.filesize_kb = filesize_kb
                upload.save()

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return custom_error_reponse('Invalid JSON', 400)
        except Upload.DoesNotExist:
            return custom_error_reponse('Upload not found', 404)
        except Exception as e:
            return custom_error_reponse(str(e), 400)
        
    return custom_error_reponse('Invalid request method', 400)


@csrf_exempt
@login_required
def list_files(request):
    uploads = Upload.objects.filter(user=request.user)
    return render(request, 'web/list_files.html', {'uploads': uploads})


@csrf_exempt
def delete_selected_files_view(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            file_ids = data.get('ids', [])
            
            # Validate file_ids
            if not isinstance(file_ids, list):
                return HttpResponseBadRequest(f'Invalid data format. Expected list, got {type(file_ids).__name__}.')
            
            # Query files to delete
            uploads_to_delete = Upload.objects.filter(id__in=file_ids)
            deleted_count = uploads_to_delete.count()
            
            # Delete files from filesystem
            for upload in uploads_to_delete:
                file_path = os.path.join(settings.MEDIA_ROOT, upload.file.name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            
            # Delete file records
            uploads_to_delete.delete()
            
            return JsonResponse({'message': f'Successfully deleted {deleted_count} files.'})

        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON format.')
        except Exception as e:
            return HttpResponseBadRequest(f'An error occurred: {str(e)}')

    return HttpResponseBadRequest('Invalid request method. Use POST.')

def upload_success(request):
    return render(request, 'web/success.html')

@login_required
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

