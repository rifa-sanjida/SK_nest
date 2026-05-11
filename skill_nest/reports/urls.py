from django.urls import path
from .views import submit_report

urlpatterns = [
    path('submit/<int:booking_id>/', submit_report, name='submit_report'),
]