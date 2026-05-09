from django.contrib import messages
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import provider_required, learner_required
from .models import (
    Service,
    ServiceCategory,
    ProviderAvailability,
    BlockedDate,
    City,
    Area,
    Division,
    Wishlist,
)
from .forms import ServiceForm, ProviderAvailabilityForm, BlockedDateForm


def service_list(request):
    services = Service.objects.filter(is_active=True)

    category = request.GET.get('category')
    division = request.GET.get('division')
    city = request.GET.get('city')
    area = request.GET.get('area')
    max_price = request.GET.get('max_price')

    if category:
        services = services.filter(category__id=category)
    if division:
        services = services.filter(division__iexact=division)
    if city:
        services = services.filter(city__iexact=city)
    if area:
        services = services.filter(area__iexact=area)
    if max_price:
        services = services.filter(price__lte=max_price)

    services = services.annotate(avg_rating=Avg('reviews__rating')).order_by('-created_at')

    categories = ServiceCategory.objects.all().order_by('name')
    divisions = Division.objects.all().order_by('name')

    cities = City.objects.none()
    areas = Area.objects.none()

    if division:
        selected_division_obj = Division.objects.filter(name=division).first()
        if selected_division_obj:
            cities = City.objects.filter(division=selected_division_obj).order_by('name')

    if city:
        selected_city_obj = City.objects.filter(name=city).first()
        if selected_city_obj:
            areas = Area.objects.filter(city=selected_city_obj).order_by('name')

    return render(request, 'services/service_list.html', {
        'services': services,
        'categories': categories,
        'divisions': divisions,
        'cities': cities,
        'areas': areas,
        'selected_category': category,
        'selected_division': division,
        'selected_city': city,
        'selected_area': area,
        'selected_max_price': max_price,
    })


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    is_wishlisted = False

    if request.user.is_authenticated and request.user.role == 'learner':
        is_wishlisted = Wishlist.objects.filter(
            learner=request.user,
            service=service
        ).exists()

    return render(request, 'services/service_detail.html', {
        'service': service,
        'is_wishlisted': is_wishlisted,
    })


@provider_required
def provider_service_list(request):
    services = Service.objects.filter(provider=request.user)
    return render(request, 'services/provider_service_list.html', {'services': services})


@provider_required
def add_service(request):
    form = ServiceForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        service = form.save(commit=False)
        service.provider = request.user
        service.save()
        messages.success(request, 'Service added successfully.')
        return redirect('provider_service_list')
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Add Service'})


@provider_required
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user)
    form = ServiceForm(request.POST or None, request.FILES or None, instance=service)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Service updated successfully.')
        return redirect('provider_service_list')
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Edit Service'})


@provider_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully.')
        return redirect('provider_service_list')
    return render(request, 'services/confirm_delete.html', {'object': service})


@provider_required
def manage_availability(request):
    availabilities = ProviderAvailability.objects.filter(provider=request.user)
    blocked_dates = BlockedDate.objects.filter(provider=request.user)

    availability_form = ProviderAvailabilityForm(request.POST or None, prefix='availability')
    blocked_form = BlockedDateForm(request.POST or None, prefix='blocked')

    if request.method == 'POST':
        if 'save_availability' in request.POST and availability_form.is_valid():
            av = availability_form.save(commit=False)
            av.provider = request.user
            av.save()
            messages.success(request, 'Availability added.')
            return redirect('manage_availability')

        if 'save_blocked' in request.POST and blocked_form.is_valid():
            bd = blocked_form.save(commit=False)
            bd.provider = request.user
            bd.save()
            messages.success(request, 'Blocked date added.')
            return redirect('manage_availability')

    return render(request, 'services/manage_availability.html', {
        'availabilities': availabilities,
        'blocked_dates': blocked_dates,
        'availability_form': availability_form,
        'blocked_form': blocked_form,
    })


@learner_required
def toggle_wishlist(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)

    wishlist_item = Wishlist.objects.filter(
        learner=request.user,
        service=service
    ).first()

    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, 'Service removed from wishlist.')
    else:
        Wishlist.objects.create(
            learner=request.user,
            service=service
        )
        messages.success(request, 'Service added to wishlist.')

    return redirect('service_detail', pk=service.id)


@learner_required
def wishlist_list(request):
    wishlist_items = Wishlist.objects.filter(
        learner=request.user
    ).select_related('service', 'service__provider', 'service__category')

    return render(request, 'services/wishlist_list.html', {
        'wishlist_items': wishlist_items
    })


def load_cities(request):
    division_id = request.GET.get('division_id')
    cities = City.objects.filter(division_id=division_id).order_by('name')
    data = [{'id': city.id, 'name': city.name} for city in cities]
    return JsonResponse(data, safe=False)


def load_areas(request):
    city_id = request.GET.get('city_id')
    areas = Area.objects.filter(city_id=city_id).order_by('name')
    data = [{'id': area.id, 'name': area.name} for area in areas]
    return JsonResponse(data, safe=False)