from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import (
    CustomUserCreationForm,
    CustomLoginForm,
    ProviderProfileForm,
    LearnerProfileForm,
    UserUpdateForm,
    PasswordRecoveryRequestForm,
)
from .models import User, PasswordRecoveryRequest


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            if user.role not in ['learner', 'provider']:
                messages.error(request, 'Invalid account type selected.')
                return redirect('register')

            if user.role == 'provider':
                user.is_active = True
                user.is_provider_verified = False

            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm

    def form_valid(self, form):
        user = form.get_user()
        if user.is_suspended:
            messages.error(self.request, 'Your account is suspended.')
            return redirect('login')
        return super().form_valid(form)


@login_required
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('home')
    return redirect('home')


@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    if request.user.role == 'provider':
        return redirect('provider_dashboard')
    if request.user.role == 'learner':
        return redirect('learner_dashboard')
    messages.error(request, 'Invalid user role.')
    return redirect('home')


@login_required
def provider_dashboard(request):
    if request.user.role != 'provider':
        messages.error(request, 'Only providers can access this page.')
        return redirect('dashboard_redirect')
    return render(request, 'accounts/provider_dashboard.html')


@login_required
def learner_dashboard(request):
    if request.user.role != 'learner':
        messages.error(request, 'Only learners can access this page.')
        return redirect('dashboard_redirect')
    return render(request, 'accounts/learner_dashboard.html')


@login_required
def profile_manage(request):
    user_form = UserUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user
    )

    profile_form = None
    if request.user.role == 'provider':
        profile_form = ProviderProfileForm(
            request.POST or None,
            instance=request.user.provider_profile
        )
    elif request.user.role == 'learner':
        profile_form = LearnerProfileForm(
            request.POST or None,
            instance=request.user.learner_profile
        )

    if request.method == 'POST':
        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_manage')

    return render(request, 'accounts/profile_manage.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def request_password_recovery(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            PasswordRecoveryRequest.objects.create(user=user)
            messages.success(
                request,
                'Recovery request submitted. Admin will provide a temporary password.'
            )
        else:
            messages.error(request, 'No account found with this email.')

        return redirect('login')

    form = PasswordRecoveryRequestForm()
    return render(request, 'accounts/request_password_recovery.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('profile_manage')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})
