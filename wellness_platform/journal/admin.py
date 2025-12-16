from django.contrib import admin
from .models import JournalEntry


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    """Admin interface for journal entries"""
    list_display = ['title', 'user', 'word_count_display', 'created_at', 'updated_at', 'is_edited']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'content', 'user__username', 'user__email']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'word_count_display', 'content_preview']
    
    fieldsets = (
        ('Entry Information', {
            'fields': ('user', 'title', 'content')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'word_count_display', 'content_preview'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user')
    
    def word_count_display(self, obj):
        """Display word count"""
        return f"{obj.get_word_count()} words"
    word_count_display.short_description = 'Word Count'
    
    def content_preview(self, obj):
        """Display content preview"""
        return obj.get_content_preview(200)
    content_preview.short_description = 'Content Preview'
    
    def is_edited(self, obj):
        """Display if entry was edited"""
        return obj.is_edited()
    is_edited.boolean = True
    is_edited.short_description = 'Edited'
