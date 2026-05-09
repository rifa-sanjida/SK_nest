from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import learner_required, provider_required
from .models import Booking, Payment
from .forms import BookingForm, PaymentForm
from services.models import Service, BlockedDate


@learner_required
def create_booking(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)

    if request.user == service.provider:
        messages.error(request, 'You cannot book your own service.')
        return redirect('service_detail', pk=service.id)

    form = BookingForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            booking = form.save(commit=False)
            booking.learner = request.user
            booking.provider = service.provider
            booking.service = service

            blocked = BlockedDate.objects.filter(
                provider=service.provider,
                blocked_date=booking.booking_date
            ).exists()

            if blocked:
                messages.error(request, 'Provider is unavailable on this date.')
                return redirect('service_detail', pk=service.id)

            booking.save()

            Payment.objects.create(
                booking=booking,
                amount=service.price
            )

            messages.success(request, 'Booking request sent successfully.')
            return redirect('learner_booking_list')
        else:
            messages.error(request, 'Please correct the form errors below.')

    return render(request, 'bookings/create_booking.html', {
        'form': form,
        'service': service
    })


@learner_required
def learner_booking_list(request):
    bookings = Booking.objects.filter(learner=request.user).order_by('-created_at')
    return render(request, 'bookings/learner_booking_list.html', {'bookings': bookings})


@provider_required
def provider_booking_list(request):
    bookings = Booking.objects.filter(provider=request.user).order_by('-created_at')
    return render(request, 'bookings/provider_booking_list.html', {'bookings': bookings})


@provider_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id, provider=request.user)
    valid_statuses = ['confirmed', 'completed', 'cancelled', 'rejected']

    if status in valid_statuses:
        booking.status = status
        booking.save()
        messages.success(request, f'Booking marked as {status}.')

    return redirect('provider_booking_list')


@learner_required
def payment_update(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, learner=request.user)
    payment = booking.payment
    form = PaymentForm(request.POST or None, instance=payment)

    if request.method == 'POST' and form.is_valid():
        payment = form.save(commit=False)
        payment.status = 'pending_verification'
        payment.save()
        messages.success(request, 'Payment information submitted.')
        return redirect('learner_booking_list')

    return render(request, 'bookings/payment_update.html', {
        'form': form,
        'booking': booking
    })