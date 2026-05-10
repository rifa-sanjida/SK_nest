from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import learner_required
from bookings.models import Booking
from .models import Review
from .forms import ReviewForm


@learner_required
def add_review(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        learner=request.user,
        status='completed'
    )

    service = booking.service
    review = Review.objects.filter(learner=request.user, service=service).first()
    form = ReviewForm(request.POST or None, instance=review)

    if request.method == 'POST' and form.is_valid():
        review_obj = form.save(commit=False)
        review_obj.learner = request.user
        review_obj.service = service
        review_obj.save()
        messages.success(request, 'Your review has been saved.')
        return redirect('learner_booking_list')

    return render(request, 'reviews/review_form.html', {
        'form': form,
        'booking': booking,
        'service': service,
    })


@learner_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, learner=request.user)

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect('learner_booking_list')

    return render(request, 'reviews/review_delete.html', {'review': review})
