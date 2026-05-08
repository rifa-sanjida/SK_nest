from django.urls import path
from .views import (
    admin_dashboard, user_management, toggle_suspend_user, verify_provider,
    service_management, delete_service_admin, booking_management,
    report_management, resolve_report, recovery_requests, send_temporary_password
)

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('users/', user_management, name='user_management'),
    path('users/toggle-suspend/<int:user_id>/', toggle_suspend_user, name='toggle_suspend_user'),
    path('users/verify-provider/<int:user_id>/', verify_provider, name='verify_provider'),
    path('services/', service_management, name='service_management'),
    path('services/delete/<int:service_id>/', delete_service_admin, name='delete_service_admin'),
    path('bookings/', booking_management, name='booking_management'),
    path('reports/', report_management, name='report_management'),
    path('reports/resolve/<int:report_id>/', resolve_report, name='resolve_report'),
    path('recovery-requests/', recovery_requests, name='recovery_requests'),
    path('recovery-requests/send-temp/<int:request_id>/', send_temporary_password, name='send_temporary_password'),
]