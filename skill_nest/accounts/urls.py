from django.urls import path
from .views import (
    register,
    CustomLoginView,
    custom_logout,
    dashboard_redirect,
    provider_dashboard,
    learner_dashboard,
    profile_manage,
    request_password_recovery,
    change_password,
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    path('provider-dashboard/', provider_dashboard, name='provider_dashboard'),
    path('learner-dashboard/', learner_dashboard, name='learner_dashboard'),
    path('profile/', profile_manage, name='profile_manage'),
    path('password-recovery/', request_password_recovery, name='request_password_recovery'),
    path('change-password/', change_password, name='change_password'),
]