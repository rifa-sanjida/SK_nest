from django.urls import path
from .views import (
    create_booking,
    learner_booking_list,
    provider_booking_list,
    update_booking_status,
    payment_update,
)

urlpatterns = [
    path('create/<int:service_id>/', create_booking, name='create_booking'),
    path('learner/', learner_booking_list, name='learner_booking_list'),
    path('provider/', provider_booking_list, name='provider_booking_list'),
    path('update-status/<int:booking_id>/<str:status>/', update_booking_status, name='update_booking_status'),
    path('payment/<int:booking_id>/', payment_update, name='payment_update'),
]