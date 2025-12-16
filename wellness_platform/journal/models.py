from django.db import models
from django.conf import settings
from django.utils import timezone
import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.nl2br import Nl2BrExtension


class JournalEntry(models.Model):
    """Model for user journal entries with Markdown support"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='journal_entries'
    )
    title = models.CharField(max_length=200, help_text="Entry title")
    content = models.TextField(help_text="Entry content in Markdown format")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Journal Entry"
        verbose_name_plural = "Journal Entries"
        ordering = ['-created_at']  # Newest first
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username} ({self.created_at.strftime('%Y-%m-%d')})"
    
    def get_content_html(self):
        """Convert Markdown content to safe HTML"""
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.tables',
                'markdown.extensions.nl2br',
                'markdown.extensions.sane_lists',
            ],
            output_format='html5'
        )
        return md.convert(self.content)
    
    def get_content_preview(self, max_length=150):
        """Get plain text preview of content"""
        # Remove markdown formatting for preview
        plain_text = self.content.replace('#', '').replace('*', '').replace('_', '').replace('`', '')
        plain_text = ' '.join(plain_text.split())  # Normalize whitespace
        
        if len(plain_text) > max_length:
            return plain_text[:max_length] + '...'
        return plain_text
    
    def get_word_count(self):
        """Get word count of the entry"""
        return len(self.content.split())
    
    def was_recently_updated(self):
        """Check if entry was updated in the last 24 hours"""
        now = timezone.now()
        return self.updated_at >= now - timezone.timedelta(days=1)
    
    def is_edited(self):
        """Check if entry was edited after creation"""
        # Allow 1 second difference to account for processing time
        return (self.updated_at - self.created_at).total_seconds() > 1
