from django.contrib import admin
from .models import Booking, Payment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'service',
        'learner',
        'provider',
        'booking_date',
        'booking_time',
        'status',
        'created_at',
    )
    list_filter = ('status', 'booking_date')
    search_fields = ('service__title', 'learner__email', 'provider__email')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'booking',
        'amount',
        'payment_method',
        'transaction_id',
        'status',
        'confirmed_at',
    )
    list_filter = ('status', 'payment_method')
    search_fields = (
        'booking__service__title',
        'booking__learner__email',
        'booking__provider__email',
        'transaction_id',
    )
