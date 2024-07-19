from django.urls import path, include 
from .views import upload_view, upload_success, upload_status

urlpatterns = [
    path('upload/', upload_view, name='upload'),
    path('success/', upload_success, name='upload_success'),
    path('status/', upload_status, name='upload_status'),

]

