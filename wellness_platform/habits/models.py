from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, date


class Habit(models.Model):
    """Model representing a user's habit"""
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    CATEGORY_CHOICES = [
        ('health', 'Health & Fitness'),
        ('mindfulness', 'Mindfulness'),
        ('productivity', 'Productivity'),
        ('learning', 'Learning'),
        ('social', 'Social'),
        ('creativity', 'Creativity'),
        ('finance', 'Finance'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='habits')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Tracking fields
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    total_completions = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_frequency_display()})"

    def get_completion_for_date(self, check_date=None):
        """Get completion record for a specific date"""
        if check_date is None:
            check_date = date.today()
        try:
            return self.completions.get(completed_date=check_date)
        except HabitCompletion.DoesNotExist:
            return None

    def is_completed_today(self):
        """Check if habit is completed today"""
        return self.get_completion_for_date() is not None

    def can_complete_today(self):
        """Check if habit can be marked as complete today"""
        return not self.is_completed_today()

    def mark_complete(self, completed_date=None):
        """Mark habit as complete for a specific date"""
        if completed_date is None:
            completed_date = date.today()

        # Check if already completed
        if self.get_completion_for_date(completed_date):
            return False, "Already completed for this date"

        # Create completion record
        completion = HabitCompletion.objects.create(
            habit=self,
            completed_date=completed_date
        )

        # Update tracking statistics
        self.update_streaks()
        self.total_completions += 1
        self.save()

        return True, "Habit marked as complete"

    def update_streaks(self):
        """Update current and longest streak based on completion history"""
        completions = self.completions.order_by('-completed_date')

        if not completions.exists():
            self.current_streak = 0
            return

        # Calculate current streak
        current_streak = 0
        check_date = date.today()

        for completion in completions:
            if completion.completed_date == check_date:
                current_streak += 1
                check_date -= timedelta(days=1)
            elif (check_date - completion.completed_date).days == 1:
                current_streak += 1
                check_date = completion.completed_date - timedelta(days=1)
            else:
                break

        self.current_streak = current_streak

        # Update longest streak if current is higher
        if current_streak > self.longest_streak:
            self.longest_streak = current_streak

    def get_completion_rate(self, days=30):
        """Calculate completion rate for the last N days"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        completions_count = self.completions.filter(
            completed_date__gte=start_date,
            completed_date__lte=end_date
        ).count()

        if self.frequency == 'daily':
            expected_completions = days
        else:  # weekly
            expected_completions = days // 7

        if expected_completions == 0:
            return 0

        return round((completions_count / expected_completions) * 100, 1)

    def get_calendar_data(self, year=None, month=None):
        """Get completion data for calendar display"""
        if year is None or month is None:
            today = date.today()
            year = today.year
            month = today.month

        # Get all completions for the month
        completions = self.completions.filter(
            completed_date__year=year,
            completed_date__month=month
        ).values_list('completed_date', flat=True)

        return set(completions)


class HabitCompletion(models.Model):
    """Model representing a habit completion on a specific date"""
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='completions')
    completed_date = models.DateField(default=date.today)
    completed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-completed_date']
        unique_together = ['habit', 'completed_date']

    def __str__(self):
        return f"{self.habit.name} - {self.completed_date}"
