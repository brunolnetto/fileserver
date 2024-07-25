# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm, AuthenticationForm,
)
from django.contrib.auth import login, authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import (
    IntegerField,  DateField, DateTimeField,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetView

from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from shutil import rmtree

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.conf import settings
from django.apps import apps

import logging
import json
import os

from .forms import CustomPasswordResetForm, UploadForm
from .utils import custom_error_response
from .models import Upload

DEFAULT_PAGE_SIZE = 5

# Get the logger
logger = logging.getLogger('django')

def get_field_type(field):
    if isinstance(field, IntegerField):
        return 'number'
    elif isinstance(field, DateField) or \
        isinstance(field, DateTimeField):
        return 'date'
    else:
        return 'string'

def table_view(request, model_name):
    # Get the model class dynamically
    try:
        ModelClass = apps.get_model('web', model_name)
    except LookupError:
        return JsonResponse({'error': 'Model not found'}, status=400)
    
    sort_field = request.GET.get('sort_field')
    sort_order = request.GET.get('sort_order', 'asc')
    objects = ModelClass.objects.all()

    if sort_field:
        if sort_order == 'asc':
            objects = objects.order_by(sort_field)
        else:
            objects = objects.order_by(f'-{sort_field}')
    
    # Get fields for the model
    fields = ModelClass._meta.get_fields()
    
    # Prepare field information for template
    field_info = [{
        'name': field.name,
        'verbose_name': field.verbose_name
    } for field in fields if field.concrete]

    # Fetch data and paginate
    objects = ModelClass.objects.all()

    paginator = Paginator(objects, DEFAULT_PAGE_SIZE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request, 'web/table_template.html', 
        {
            'model_name': model_name,
            'fields': field_info,
            'objects': page_obj,
        }
    )

@require_POST
def update_data(request, model_name):
    try:
        # Get the model class
        model = apps.get_model('web', model_name)
    except LookupError:
        return JsonResponse({'error': 'Model not found'}, status=400)
    except AttributeError:
        return JsonResponse({'error': 'Model does not have a get_column_labels method'}, status=400)

    # Parse the JSON request body
    data = json.loads(request.body)
    updates = data.get('updates', [])

    for update in updates:
        try:
            
            # Get the object to be updated
            obj = model.objects.get(id=update['id'])
            
            for field_name, value in update.items():
                # Skip the 'id' field
                if field_name == 'id':
                    continue

                # Translate label to database field name
                if field_name:
                    setattr(obj, field_name, value)
                    print(f'Setting {field_name} to {value}')
            
            obj.save()
        except model.DoesNotExist:
            print(f'Object with id {update["id"]} does not exist')
            continue
        except Exception as e:
            print(f'Error updating object: {e}')
            return JsonResponse({'error': 'Error updating object'}, status=500)

    return JsonResponse({'status': 'success'})

@csrf_exempt
@require_POST
def delete_selected_files_view(request, model_name):
    try:
        # Get the model class based on the model_name
        model = apps.get_model('web', model_name)
    except LookupError:
        logger.error(f"Model not found: {model_name}")
        return JsonResponse({'error': 'Model not found'}, status=400)

    try:
        # Load and parse JSON data from the request body
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    ids = data.get('ids', [])
    logger.debug(f"Received IDs to delete: {ids}")

    if not ids:
        return JsonResponse({'status': 'success', 'message': 'No IDs provided'})

    # Convert IDs to the correct type if necessary (e.g., integers)
    ids = [int(id) for id in ids]  # Modify this line based on the actual ID type

    # Query objects to delete
    objects = model.objects.filter(id__in=ids)

    if not objects.exists():
        logger.debug(f"No objects found with IDs: {ids}")
        return JsonResponse({'status': 'success', 'message': 'No objects found with the provided IDs'})

    # Get the field name for the file
    file_field_name = model.get_delete_field()
    logger.debug(f"File field name: {file_field_name}")

    if file_field_name:
        # Ensure the model has the file field
        if hasattr(model, file_field_name):
            
            # Delete associated files
            for obj in objects:
                # Construct the file path
                file_field = getattr(obj, file_field_name)
                if file_field:
                    file_path = os.path.join(settings.MEDIA_ROOT, file_field.name)
                    logger.debug(f"Checking file path: {file_path}")
                    if os.path.isfile(file_path):
                        try:
                            os.remove(file_path)
                            logger.debug(f"Successfully deleted file: {file_path}")
                        except Exception as e:
                            logger.error(f"Error deleting file {file_path}: {str(e)}")
                    else:
                        logger.warning(f"File not found: {file_path}")
        else:
            logger.error(f"Model does not have a field named: {file_field_name}")

    # Delete database entries
    deleted_count, _ = model.objects.filter(id__in=ids).delete()
    logger.debug(f"Number of objects deleted from database: {deleted_count}")
    
    return JsonResponse({'status': 'success'})
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset_form.html'

def home_view(request):
    return render(request, 'web/home.html')

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('home')
    
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
@require_POST
def check_username_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username', '')
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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
def check_email_view(request):
    email = request.POST.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})

@login_required
@csrf_exempt
@require_POST
def update_first_login_flag(request):
    user_profile = request.user.userprofile
    if user_profile.first_login:
        user_profile.first_login = False
        user_profile.save()
        return JsonResponse({'status': 'success'})

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
            return custom_error_response('No files uploaded', 400)

        # Get the current user
        user = request.user

        # Iterate over each file and process it
        for file in files:
            # Validate file type
            if not validate_file_type(file.name):
                return custom_error_response(f'Invalid file type: {file.name}', status=400)

            # Save the file (assuming Upload model has a `file` field and a `user` foreign key field)
            upload = Upload(
                uplo_filename=file.name,
                uplo_filesize=file.size,
                # TODO: Add description on upload if possible
                uplo_description='',
                uplo_file=file, 
                uplo_user=user
            )
            upload.save()

        return JsonResponse({'status': 'success'})

    # Render the upload page for GET request
    return render(request, 'web/upload.html')


@csrf_exempt
def update_uploaded_files_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            updates = data.get('updates', [])

            for item in updates:
                upload_id = item.get('id')
                file = item.get('file')
                filesize_kb = item.get('filesize_kb')

                if not all([upload_id, file, filesize_kb is not None]):
                    return custom_error_response('Missing data', 400)

                upload = Upload.objects.get(uplo_id=upload_id)
                upload.file = file
                upload.filesize_kb = filesize_kb
                upload.save()

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return custom_error_response('Invalid JSON', 400)
        except Upload.DoesNotExist:
            return custom_error_response('Upload not found', 404)
        except Exception as e:
            return custom_error_response(str(e), 400)
        
    return custom_error_response('Invalid request method', 400)


def upload_success_view(request):
    return render(request, 'web/success.html')

@login_required
def upload_status_view(request):
    uploads_list = Upload.objects.all()
    
    # Convert filesize from bytes to megabytes
    for upload in uploads_list:
        # Convert to MB
        upload.filesize_kb = upload.uplo_filesize / 1024
    
    # Show 10 uploads per page
    paginator = Paginator(uploads_list, DEFAULT_PAGE_SIZE)  

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

