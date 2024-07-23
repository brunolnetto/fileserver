from django.urls import path, include 
from django.conf.urls import handler400, handler403, handler404, handler500
from django.http import HttpResponseNotFound
from django.contrib.auth import views as auth_views

from .views import (
    home_view, 
    upload_files_view, update_uploads, upload_success, upload_status, 
    delete_selected_files_view, signup_view, login_view, logout_view, settings_view, 
    check_username, check_email, login_required_view,
)
from django.conf.urls import handler400, handler403, handler404, handler500

handler400 = 'web.views.custom_bad_request'
handler403 = 'web.views.custom_permission_denied'
handler404 = 'web.views.custom_page_not_found'
handler500 = 'web.views.custom_server_error'

urlpatterns = [
    path('', home_view, name='home'), 
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('settings/', settings_view, name='settings'),
    path('login_required/', login_required_view, name='login_required'),
    path('delete-selected-files/', delete_selected_files_view, name='delete_selected_files'),
    path('upload-files/', upload_files_view, name='upload_files'),
    path('update-uploads/', update_uploads, name='update_uploads'),
    path('check-username/', check_username, name='check-username'),
    path('check-email/', check_email, name='check_email'),
    path('success/', upload_success, name='upload_success'),
    path('status/', upload_status, name='upload_status'),
]

