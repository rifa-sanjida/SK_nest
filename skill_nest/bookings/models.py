from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from services.models import Service


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    )

    learner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='learner_bookings'
    )
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='provider_bookings'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Do not validate overlap until required fields are assigned
        if not self.provider_id or not self.booking_date or not self.booking_time:
            return

        overlapping = Booking.objects.filter(
            provider_id=self.provider_id,
            booking_date=self.booking_date,
            booking_time=self.booking_time,
        ).exclude(pk=self.pk).exclude(status__in=['cancelled', 'rejected'])

        if overlapping.exists():
            raise ValidationError('This provider already has a booking at that date and time.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        service_title = self.service.title if self.service_id else 'No Service'
        learner_email = self.learner.email if self.learner_id else 'No Learner'
        return f"{service_title} - {learner_email}"


class Payment(models.Model):
    PAYMENT_STATUS = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('pending_verification', 'Pending Verification'),
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='cash')
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=30, choices=PAYMENT_STATUS, default='unpaid')
    confirmed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment for Booking #{self.booking.id}"