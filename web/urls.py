from django.urls import path, include 
from django.conf.urls import handler400, handler403, handler404, handler500
from django.http import HttpResponseNotFound

from .views import (
    home_view, upload_files, upload_success, delete_selected_uploads, upload_status,
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
    path('success/', upload_success, name='upload_success'),
    path('status/', upload_status, name='upload_status'),
    path('simulate-404/', lambda request: HttpResponseNotFound("This page does not exist.")),
]

