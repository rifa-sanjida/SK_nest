from django.urls import path
from .views import conversation_list, conversation_detail

urlpatterns = [
    path('inbox/', conversation_list, name='inbox'),
    path('chat/<int:user_id>/', conversation_detail, name='conversation_detail'),
]