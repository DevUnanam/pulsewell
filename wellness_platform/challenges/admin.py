from django.contrib import admin
from .models import Challenge, UserChallenge, DailyCheckIn, ChallengeBadge


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'goal_type', 'duration_days', 'is_active', 'is_featured', 'get_participant_count', 'created_at']
    list_filter = ['difficulty', 'goal_type', 'is_active', 'is_featured', 'tracking_type']
    search_fields = ['title', 'description', 'daily_requirement']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'get_participant_count', 'get_completion_rate']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'cover_image')
        }),
        ('Challenge Configuration', {
            'fields': ('duration_days', 'difficulty', 'goal_type', 'tracking_type', 'daily_target', 'daily_requirement')
        }),
        ('Rewards & Gamification', {
            'fields': ('points_reward', 'badge_name', 'badge_icon')
        }),
        ('Visibility & Limits', {
            'fields': ('is_active', 'is_featured', 'max_participants')
        }),
        ('Smart Recommendations', {
            'fields': ('recommended_for_bmi_range', 'recommended_for_goals'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at', 'get_participant_count', 'get_completion_rate'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new challenge
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'status', 'start_date', 'end_date', 'days_completed', 'completion_percentage', 'current_streak']
    list_filter = ['status', 'challenge', 'start_date']
    search_fields = ['user__username', 'challenge__title']
    readonly_fields = ['joined_at', 'completed_at', 'completion_percentage', 'longest_streak']

    fieldsets = (
        ('User & Challenge', {
            'fields': ('user', 'challenge', 'status')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'joined_at', 'completed_at')
        }),
        ('Progress', {
            'fields': ('days_completed', 'completion_percentage', 'current_streak', 'longest_streak')
        }),
        ('Rewards', {
            'fields': ('points_earned', 'badge_earned')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )


@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = ['user_challenge', 'date', 'completed', 'value_logged', 'mood', 'difficulty', 'checked_in_at']
    list_filter = ['completed', 'mood', 'difficulty', 'date']
    search_fields = ['user_challenge__user__username', 'user_challenge__challenge__title']
    readonly_fields = ['checked_in_at']
    date_hierarchy = 'date'


@admin.register(ChallengeBadge)
class ChallengeBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge_name', 'badge_icon', 'challenge', 'earned_at']
    list_filter = ['challenge', 'earned_at']
    search_fields = ['user__username', 'badge_name']
    readonly_fields = ['earned_at']
    date_hierarchy = 'earned_at'
