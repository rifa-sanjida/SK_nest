from django.contrib import messages
from django.shortcuts import redirect


def provider_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in first.')
            return redirect('login')

        if request.user.role != 'provider':
            messages.error(request, 'Only providers can access this page.')
            return redirect('dashboard_redirect')

        return view_func(request, *args, **kwargs)
    return wrapper


def learner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in first.')
            return redirect('login')

        if request.user.role != 'learner':
            messages.error(request, 'Only learners can access this page.')
            return redirect('dashboard_redirect')

        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in first.')
            return redirect('login')

        if not request.user.is_staff:
            messages.error(request, 'Only admin can access this page.')
            return redirect('dashboard_redirect')

        return view_func(request, *args, **kwargs)
    return wrapper