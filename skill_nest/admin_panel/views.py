import random
import string
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from services.models import Service
from bookings.models import Booking, Payment
from reports.models import Report
from accounts.models import PasswordRecoveryRequest

User = get_user_model()


def generate_temp_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@staff_member_required
def admin_dashboard(request):
    context = {
        'users_count': User.objects.count(),
        'providers_count': User.objects.filter(role='provider').count(),
        'learners_count': User.objects.filter(role='learner').count(),
        'services_count': Service.objects.count(),
        'bookings_count': Booking.objects.count(),
        'reports_count': Report.objects.count(),
    }
    return render(request, 'admin_panel/dashboard.html', context)


@staff_member_required
def user_management(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/user_management.html', {'users': users})



@staff_member_required
def toggle_suspend_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_suspended = not user.is_suspended
    user.save()
    messages.success(request, 'User status updated.')
    return redirect('user_management')



@staff_member_required
def verify_provider(request, user_id):
    user = get_object_or_404(User, id=user_id, role='provider')
    user.is_provider_verified = True
    user.save()
    messages.success(request, 'Provider verified successfully.')
    return redirect('user_management')



@staff_member_required
def service_management(request):
    services = Service.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/service_management.html', {'services': services})


@staff_member_required
def delete_service_admin(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    messages.success(request, 'Service deleted.')
    return redirect('service_management')



@staff_member_required
def booking_management(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/booking_management.html', {'bookings': bookings})


@staff_member_required
def report_management(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/report_management.html', {'reports': reports})


@staff_member_required
def resolve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.resolved = True
    report.save()
    messages.success(request, 'Report marked as resolved.')
    return redirect('report_management')


@staff_member_required
def recovery_requests(request):
    requests_list = PasswordRecoveryRequest.objects.filter(is_resolved=False).order_by('-requested_at')
    return render(request, 'admin_panel/recovery_requests.html', {'requests_list': requests_list})



@staff_member_required
def send_temporary_password(request, request_id):
    recovery = get_object_or_404(PasswordRecoveryRequest, id=request_id, is_resolved=False)
    temp_password = generate_temp_password()
    user = recovery.user
    user.set_password(temp_password)
    user.temporary_password_sent = True
    user.save()

    recovery.temporary_password = temp_password
    recovery.is_resolved = True
    recovery.save()

    messages.success(request, f'Temporary password generated for {user.email}: {temp_password}')
    return redirect('recovery_requests')
