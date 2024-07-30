from django.urls import path 
from django.conf.urls import handler400, handler403, handler404, handler500
from django.contrib.auth import views as auth_views
0
from .views import (
    home_view, table_view, update_data, confirm_email,
    upload_files_view, update_uploaded_files_view, upload_success_view, upload_status_view, 
    delete_selected_files_view, signup_view, login_view, logout_view, settings_view, 
    check_email, check_username, login_required_view, update_first_login_flag,
)
from .views import send_test_email
from .views import CustomPasswordResetView

handler400 = 'web.views.custom_bad_request'
handler403 = 'web.views.custom_permission_denied'
handler404 = 'web.views.custom_page_not_found'
handler500 = 'web.views.custom_server_error'

urlpatterns = [
    path('', home_view, name='home'), 
    # Registration routes
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('settings/', settings_view, name='settings'),
    path('login_required/', login_required_view, name='login_required'),
    path('update-first-login-flag/', update_first_login_flag, name='update_first_login_flag'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('confirm_email/<uidb64>/<token>/', confirm_email, name='confirm_email'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('check-username/', check_username, name='check-username'),
    path('check-email/', check_email, name='check-email'),
    path('send-test-email/', send_test_email, name='send_test_email'),
    # File upload routes
    path('upload-files/', upload_files_view, name='upload_files'),
    path('update-files/', update_uploaded_files_view, name='update_files'),
    path('delete-selected-files/', delete_selected_files_view, name='delete_selected_files'),
    path('success/', upload_success_view, name='upload_success'),
    path('status-files/', upload_status_view, name='upload_status'),
    # Table routes
    path('table/<str:model_name>/', table_view, name='table_view'),
    path('update_data/<str:model_name>/', update_data, name='update_data'),
    path('delete_selected_data/<str:model_name>/', delete_selected_files_view, name='delete_selected_data'),
]

