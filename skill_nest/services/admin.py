from django.contrib import admin
from .models import (
    Division,
    City,
    Area,
    ServiceCategory,
    Service,
    Wishlist,
    ProviderAvailability,
    BlockedDate,
)


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'division')
    list_filter = ('division',)
    search_fields = ('name', 'division__name')


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    list_filter = ('city', 'city__division')
    search_fields = ('name', 'city__name', 'city__division__name')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'provider', 'category', 'price', 'division', 'city', 'area', 'is_active')
    list_filter = ('category', 'division', 'city', 'area', 'is_active')
    search_fields = ('title', 'provider__email', 'provider__username')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'learner', 'service', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('learner__email', 'service__title')


@admin.register(ProviderAvailability)
class ProviderAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'day_of_week', 'start_time', 'end_time')


@admin.register(BlockedDate)
class BlockedDateAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'blocked_date', 'reason')
