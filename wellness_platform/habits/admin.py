from django.contrib import admin
from .models import Habit, HabitCompletion


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'frequency', 'category', 'current_streak', 'longest_streak', 'total_completions', 'is_active', 'created_at']
    list_filter = ['frequency', 'category', 'is_active', 'created_at']
    search_fields = ['name', 'user__username', 'description']
    readonly_fields = ['current_streak', 'longest_streak', 'total_completions', 'created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'description', 'frequency', 'category')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Statistics', {
            'fields': ('current_streak', 'longest_streak', 'total_completions', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HabitCompletion)
class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ['habit', 'completed_date', 'completed_at']
    list_filter = ['completed_date', 'completed_at']
    search_fields = ['habit__name', 'habit__user__username', 'notes']
    date_hierarchy = 'completed_date'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('habit', 'habit__user')
