from django.urls import path, include 
from django.conf.urls import handler400, handler403, handler404, handler500
from django.http import HttpResponseNotFound

from .views import (
    home_view, 
    upload_files, update_uploads, upload_success, upload_status, delete_selected_uploads,
)
from django.conf.urls import handler400, handler403, handler404, handler500

handler400 = 'web.views.custom_bad_request'
handler403 = 'web.views.custom_permission_denied'
handler404 = 'web.views.custom_page_not_found'
handler500 = 'web.views.custom_server_error'

urlpatterns = [
    path('', home_view, name='home'), 
    path('upload/', upload_files, name='upload_files'),
    path('delete-selected-uploads/', delete_selected_uploads, name='delete_selected_uploads'),
    path('update-uploads/', update_uploads, name='update_uploads'),
    path('success/', upload_success, name='upload_success'),
    path('status/', upload_status, name='upload_status')
]

