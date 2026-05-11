from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from bookings.models import Booking
from .forms import ReportForm


@login_required
def submit_report(request, booking_id):
    if request.user.role == 'learner':
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            learner=request.user,
            status='completed'
        )
        reported_user = booking.provider

    elif request.user.role == 'provider':
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            provider=request.user,
            status='completed'
        )
        reported_user = booking.learner

    else:
        messages.error(request, 'Only learners and providers can submit reports.')
        return redirect('dashboard_redirect')

    form = ReportForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        report = form.save(commit=False)
        report.reporter = request.user
        report.reported_user = reported_user
        report.booking = booking
        report.service = booking.service
        report.save()
        messages.success(request, 'Your report has been submitted successfully.')
        return redirect('dashboard_redirect')

    return render(request, 'reports/submit_report.html', {
        'form': form,
        'booking': booking,
        'reported_user': reported_user,
    })
