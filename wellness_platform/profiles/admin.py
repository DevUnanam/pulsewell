from django.contrib import admin
from .models import UserProfile, Tag


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'gender', 'created_at', 'updated_at']
    list_filter = ['gender', 'unit_preference', 'profile_visibility', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number', 'city', 'country']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Profile Picture', {
            'fields': ('profile_picture',)
        }),
        ('Personal Information', {
            'fields': ('phone_number', 'date_of_birth', 'gender')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country'),
            'classes': ('collapse',)
        }),
        ('Health & Wellness', {
            'fields': ('height', 'weight', 'unit_preference', 'bio', 'wellness_goals', 'medical_conditions', 'allergies')
        }),
        ('Interests', {
            'fields': ('interests',)
        }),
        ('Privacy', {
            'fields': ('profile_visibility', 'show_email')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
