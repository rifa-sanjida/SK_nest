from django.urls import path
from .views import add_review, delete_review

urlpatterns = [
    path('add/<int:booking_id>/', add_review, name='add_review'),
    path('delete/<int:review_id>/', delete_review, name='delete_review'),
]