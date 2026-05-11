from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter', 'reported_user', 'service', 'reason', 'resolved', 'created_at')
    list_filter = ('reason', 'resolved', 'created_at')
    search_fields = ('reporter__email', 'reported_user__email', 'service__title', 'details')