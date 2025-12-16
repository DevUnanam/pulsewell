from django.contrib import admin
from .models import MoodEntry


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'mood', 'entry_date', 'created_at']
    list_filter = ['mood', 'entry_date', 'created_at']
    search_fields = ['user__username', 'note']
    date_hierarchy = 'entry_date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Entry Information', {
            'fields': ('user', 'mood', 'entry_date')
        }),
        ('Additional Details', {
            'fields': ('note',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
