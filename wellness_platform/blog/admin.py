from django.contrib import admin
from .models import Article, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin interface for managing blog articles
    """
    list_display = [
        'title',
        'author',
        'published',
        'comment_count',
        'likes_count',
        'created_at',
        'reading_time_display'
    ]
    list_filter = ['published', 'created_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'comment_count', 'likes_count']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Article Information', {
            'fields': ('title', 'slug', 'author', 'published')
        }),
        ('Content', {
            'fields': ('content',),
            'description': 'Write your article content in Markdown format'
        }),
        ('Media', {
            'fields': ('image', 'video'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('comment_count', 'likes_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def reading_time_display(self, obj):
        """Display reading time in admin"""
        return f"{obj.get_reading_time()} min"
    reading_time_display.short_description = 'Reading Time'

    def save_model(self, request, obj, form, change):
        """Set author to current user if creating new article"""
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface for managing comments
    """
    list_display = [
        'user',
        'article',
        'content_preview',
        'is_reply',
        'likes_count_display',
        'created_at'
    ]
    list_filter = ['created_at', 'article']
    search_fields = ['content', 'user__username', 'article__title']
    readonly_fields = ['created_at', 'updated_at', 'likes_count_display']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Comment Information', {
            'fields': ('article', 'user', 'parent')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Metadata', {
            'fields': ('likes_count_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        """Display preview of comment content"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

    def likes_count_display(self, obj):
        """Display likes count"""
        return obj.get_likes_count()
    likes_count_display.short_description = 'Likes'

    def has_add_permission(self, request):
        """Only allow adding comments through the frontend"""
        return False
