from django.urls import path
from .views import (
    service_list,
    service_detail,
    provider_service_list,
    add_service,
    edit_service,
    delete_service,
    manage_availability,
    toggle_wishlist,
    wishlist_list,
    load_cities,
    load_areas,
)

urlpatterns = [
    path('', service_list, name='service_list'),
    path('<int:pk>/', service_detail, name='service_detail'),

    path('provider/my-services/', provider_service_list, name='provider_service_list'),
    path('provider/add/', add_service, name='add_service'),
    path('provider/<int:pk>/edit/', edit_service, name='edit_service'),
    path('provider/<int:pk>/delete/', delete_service, name='delete_service'),
    path('provider/availability/', manage_availability, name='manage_availability'),

    path('wishlist/', wishlist_list, name='wishlist_list'),
    path('wishlist/toggle/<int:service_id>/', toggle_wishlist, name='toggle_wishlist'),

    path('ajax/load-cities/', load_cities, name='load_cities'),
    path('ajax/load-areas/', load_areas, name='load_areas'),
]