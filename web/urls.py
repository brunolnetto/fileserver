from django.urls import path, include 
from .views import (
    home_view, upload_view, upload_success, delete_selected_uploads, upload_status,
)

urlpatterns = [
    path('', home_view, name='home'), 
    path('upload/', upload_view, name='upload_base'),
    path('delete-selected-uploads/', delete_selected_uploads, name='delete_selected_uploads'),
    path('success/', upload_success, name='upload_success'),
    path('status/', upload_status, name='upload_status'),
]

