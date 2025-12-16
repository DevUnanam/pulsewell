from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date


class MoodEntry(models.Model):
    """Model representing a user's daily mood entry"""

    MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ('calm', '😌 Calm'),
        ('neutral', '😐 Neutral'),
        ('sad', '😢 Sad'),
        ('stressed', '😰 Stressed'),
        ('anxious', '😟 Anxious'),
        ('energetic', '⚡ Energetic'),
        ('tired', '😴 Tired'),
    ]

    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='mood_entries')
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    note = models.TextField(blank=True, null=True, help_text="Optional: Add a short note about how you're feeling")
    entry_date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-entry_date', '-created_at']
        unique_together = ['user', 'entry_date']
        verbose_name = 'Mood Entry'
        verbose_name_plural = 'Mood Entries'

    def __str__(self):
        return f"{self.user.username} - {self.get_mood_display()} on {self.entry_date}"

    def get_mood_emoji(self):
        """Return just the emoji from the mood choice"""
        mood_dict = dict(self.MOOD_CHOICES)
        return mood_dict.get(self.mood, '').split()[0] if self.mood in mood_dict else ''

    def get_mood_name(self):
        """Return just the name from the mood choice"""
        mood_dict = dict(self.MOOD_CHOICES)
        full_text = mood_dict.get(self.mood, '')
        return ' '.join(full_text.split()[1:]) if full_text else ''

    @classmethod
    def get_today_mood(cls, user):
        """Get today's mood entry for a user"""
        try:
            return cls.objects.get(user=user, entry_date=date.today())
        except cls.DoesNotExist:
            return None

    @classmethod
    def has_logged_today(cls, user):
        """Check if user has logged mood today"""
        return cls.objects.filter(user=user, entry_date=date.today()).exists()
