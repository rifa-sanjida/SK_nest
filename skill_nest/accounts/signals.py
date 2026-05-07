from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, ProviderProfile, LearnerProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'provider':
            ProviderProfile.objects.create(user=instance)
        elif instance.role == 'learner':
            LearnerProfile.objects.create(user=instance)