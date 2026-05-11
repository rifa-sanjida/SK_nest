from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from bookings.models import Booking
from .models import Message
from .forms import ChatMessageForm

User = get_user_model()


def users_can_chat(current_user, other_user):
    if current_user == other_user:
        return False

    roles = {current_user.role, other_user.role}
    if roles != {'learner', 'provider'}:
        return False

    if current_user.role == 'learner':
        learner = current_user
        provider = other_user
    else:
        learner = other_user
        provider = current_user

    return Booking.objects.filter(
        learner=learner,
        provider=provider
    ).exclude(status__in=['cancelled', 'rejected']).exists()


def conversation_list(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in first.')
        return redirect('login')

    partners = []

    if request.user.role == 'learner':
        booking_users = [
            booking.provider for booking in Booking.objects.filter(
                learner=request.user
            ).exclude(status__in=['cancelled', 'rejected']).select_related('provider')
        ]
    elif request.user.role == 'provider':
        booking_users = [
            booking.learner for booking in Booking.objects.filter(
                provider=request.user
            ).exclude(status__in=['cancelled', 'rejected']).select_related('learner')
        ]
    else:
        booking_users = []

    message_users = list(
        User.objects.filter(
            Q(sent_messages__receiver=request.user) |
            Q(received_messages__sender=request.user)
        ).distinct()
    )

    seen_ids = set()
    for user_obj in booking_users + message_users:
        if user_obj.id != request.user.id and user_obj.id not in seen_ids:
            seen_ids.add(user_obj.id)
            unread_count = Message.objects.filter(
                sender=user_obj,
                receiver=request.user,
                is_read=False
            ).count()
            last_message = Message.objects.filter(
                Q(sender=request.user, receiver=user_obj) |
                Q(sender=user_obj, receiver=request.user)
            ).order_by('-created_at').first()

            partners.append({
                'user': user_obj,
                'unread_count': unread_count,
                'last_message': last_message,
            })

    return render(request, 'messaging/inbox.html', {'partners': partners})


def conversation_detail(request, user_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in first.')
        return redirect('login')

    other_user = get_object_or_404(User, id=user_id)

    if not users_can_chat(request.user, other_user):
        messages.error(request, 'You are not allowed to chat with this user.')
        return redirect('inbox')

    chat_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')

    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    form = ChatMessageForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        new_message = form.save(commit=False)
        new_message.sender = request.user
        new_message.receiver = other_user
        new_message.save()
        return redirect('conversation_detail', user_id=other_user.id)

    return render(request, 'messaging/conversation_detail.html', {
        'other_user': other_user,
        'chat_messages': chat_messages,
        'form': form,
    })
