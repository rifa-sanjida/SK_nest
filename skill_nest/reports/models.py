from django.db import models
from django.conf import settings
from bookings.models import Booking
from services.models import Service


class Report(models.Model):
    REPORT_TYPES = (
        ('fraud', 'Fraud'),
        ('abuse', 'Abuse'),
        ('inappropriate_content', 'Inappropriate Content'),
        ('misbehavior', 'Misbehavior'),
        ('other', 'Other'),
    )

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submitted_reports'
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_against',
        null=True,
        blank=True
    )
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='reports',
        null=True,
        blank=True
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        related_name='reports',
        null=True,
        blank=True
    )
    reason = models.CharField(max_length=50, choices=REPORT_TYPES)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        reported = self.reported_user.email if self.reported_user else 'Unknown User'
        return f"Report by {self.reporter.email} against {reported}"
