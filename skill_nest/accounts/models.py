from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('learner', 'Learner'),
        ('provider', 'Provider'),
        ('admin_user', 'Admin User'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='learner')
    email = models.EmailField(unique=True)

    division = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    is_provider_verified = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    temporary_password_sent = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"


class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    certifications = models.TextField(blank=True)
    skill_description = models.TextField(blank=True)
    contact_info = models.TextField(blank=True)
    visibility_status = models.BooleanField(default=True)
    weekly_schedule = models.TextField(blank=True)

    def __str__(self):
        return f"ProviderProfile - {self.user.email}"


class LearnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learner_profile')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"LearnerProfile - {self.user.email}"


class PasswordRecoveryRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    temporary_password = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Recovery request for {self.user.email}"
