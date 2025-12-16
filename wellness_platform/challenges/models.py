from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator


class Challenge(models.Model):
    """Main Challenge Model - Created by admins"""

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    GOAL_TYPE_CHOICES = [
        ('weight', 'Weight Loss'),
        ('fitness', 'Fitness & Strength'),
        ('mental_health', 'Mental Health'),
        ('nutrition', 'Nutrition & Diet'),
        ('sleep', 'Sleep Quality'),
        ('hydration', 'Hydration'),
        ('flexibility', 'Flexibility'),
        ('endurance', 'Endurance'),
        ('mindfulness', 'Mindfulness'),
        ('general', 'General Wellness'),
    ]

    TRACKING_TYPE_CHOICES = [
        ('boolean', 'Yes/No (Completed or Not)'),
        ('numeric', 'Numeric (e.g., steps, calories)'),
        ('time', 'Time-based (e.g., minutes)'),
        ('count', 'Count (e.g., glasses of water)'),
    ]

    # Basic Information
    title = models.CharField(max_length=200, help_text='Challenge name')
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(help_text='Detailed description of the challenge')
    short_description = models.CharField(max_length=150, help_text='Brief summary for cards')

    # Challenge Properties
    duration_days = models.PositiveIntegerField(help_text='Challenge duration in days')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES, default='general')

    # Tracking Configuration
    tracking_type = models.CharField(max_length=20, choices=TRACKING_TYPE_CHOICES, default='boolean')
    daily_target = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Daily target value (for numeric/time/count tracking)'
    )
    daily_requirement = models.TextField(help_text='What users need to do daily (e.g., "Walk 10,000 steps")')

    # Rewards
    points_reward = models.PositiveIntegerField(default=100, help_text='Points earned on completion')
    badge_name = models.CharField(max_length=100, blank=True, help_text='Badge name for completion')
    badge_icon = models.CharField(max_length=50, blank=True, help_text='Emoji or icon for badge')

    # Visibility & Status
    is_active = models.BooleanField(default=True, help_text='Is challenge available to join?')
    is_featured = models.BooleanField(default=False, help_text='Feature on homepage?')
    max_participants = models.PositiveIntegerField(null=True, blank=True, help_text='Max users (optional)')

    # Personalization Tags (for smart recommendations)
    recommended_for_bmi_range = models.CharField(
        max_length=50,
        blank=True,
        help_text='e.g., "18.5-25" or "25-30"'
    )
    recommended_for_goals = models.JSONField(
        default=list,
        blank=True,
        help_text='List of wellness goals this suits'
    )

    # Images
    cover_image = models.ImageField(upload_to='challenges/covers/', null=True, blank=True)

    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_challenges')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Challenge'
        verbose_name_plural = 'Challenges'
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def get_participant_count(self):
        """Get number of users who joined this challenge"""
        return self.user_challenges.filter(status__in=['active', 'completed']).count()

    def is_full(self):
        """Check if challenge has reached max participants"""
        if self.max_participants:
            return self.get_participant_count() >= self.max_participants
        return False

    def get_completion_rate(self):
        """Calculate percentage of users who completed the challenge"""
        total = self.user_challenges.count()
        if total == 0:
            return 0
        completed = self.user_challenges.filter(status='completed').count()
        return round((completed / total) * 100, 1)


class UserChallenge(models.Model):
    """User's participation in a challenge"""

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('abandoned', 'Abandoned'),
    ]

    # Relationships
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_challenges')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='user_challenges')

    # Dates & Status
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # Progress Tracking
    current_streak = models.PositiveIntegerField(default=0, help_text='Current consecutive days completed')
    longest_streak = models.PositiveIntegerField(default=0, help_text='Longest streak achieved')
    days_completed = models.PositiveIntegerField(default=0, help_text='Total days completed')
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Rewards
    points_earned = models.PositiveIntegerField(default=0)
    badge_earned = models.BooleanField(default=False)

    # Metadata
    joined_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text='User notes about the challenge')

    class Meta:
        verbose_name = 'User Challenge'
        verbose_name_plural = 'User Challenges'
        ordering = ['-joined_at']
        unique_together = [['user', 'challenge', 'start_date']]

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"

    def save(self, *args, **kwargs):
        # Auto-calculate end date if not set
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.challenge.duration_days)

        # Update completion percentage
        if self.challenge.duration_days > 0:
            self.completion_percentage = (self.days_completed / self.challenge.duration_days) * 100

        # Check if completed
        if self.days_completed >= self.challenge.duration_days and self.status == 'active':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.badge_earned = True
            self.points_earned = self.challenge.points_reward

        super().save(*args, **kwargs)

    def is_active(self):
        """Check if challenge is still active"""
        return self.status == 'active' and self.end_date >= timezone.now().date()

    def days_remaining(self):
        """Calculate days remaining in challenge"""
        if self.status != 'active':
            return 0
        remaining = (self.end_date - timezone.now().date()).days
        return max(0, remaining)

    def update_streak(self, completed_today):
        """Update streak based on daily check-in"""
        if completed_today:
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        else:
            self.current_streak = 0
        self.save()


class DailyCheckIn(models.Model):
    """Daily progress tracking for a user challenge"""

    MOOD_CHOICES = [
        ('excited', '😄 Excited'),
        ('motivated', '💪 Motivated'),
        ('normal', '😊 Normal'),
        ('tired', '😴 Tired'),
        ('struggling', '😓 Struggling'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('hard', 'Hard'),
        ('very_hard', 'Very Hard'),
    ]

    # Relationships
    user_challenge = models.ForeignKey(UserChallenge, on_delete=models.CASCADE, related_name='check_ins')

    # Check-in Data
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False, help_text='Did user complete the requirement?')

    # For numeric/time/count tracking
    value_logged = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Actual value achieved (steps, minutes, etc.)'
    )

    # User Feedback
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, blank=True)
    notes = models.TextField(blank=True, help_text='Optional notes about the day')

    # Metadata
    checked_in_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Daily Check-In'
        verbose_name_plural = 'Daily Check-Ins'
        ordering = ['-date']
        unique_together = [['user_challenge', 'date']]

    def __str__(self):
        return f"{self.user_challenge.user.username} - {self.user_challenge.challenge.title} - {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update UserChallenge progress
        if self.completed:
            user_challenge = self.user_challenge
            user_challenge.days_completed = user_challenge.check_ins.filter(completed=True).count()
            user_challenge.save()
            user_challenge.update_streak(True)


class ChallengeBadge(models.Model):
    """Badges earned by users for completing challenges"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    user_challenge = models.ForeignKey(UserChallenge, on_delete=models.CASCADE)

    badge_name = models.CharField(max_length=100)
    badge_icon = models.CharField(max_length=50)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Challenge Badge'
        verbose_name_plural = 'Challenge Badges'
        ordering = ['-earned_at']

    def __str__(self):
        return f"{self.user.username} - {self.badge_name}"
