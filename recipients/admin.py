from django.contrib import admin
from .models import Recipients


@admin.register(Recipients)
class RecipientsAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'relationship', 'gender', 'age_range', 'price_range')
    list_filter = ('event_type', 'gender', 'price_range')
    search_fields = ('user__email', 'relationship')
