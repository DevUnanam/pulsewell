from django import forms
from .models import Challenge, DailyCheckIn


class ChallengeForm(forms.ModelForm):
    """Form for creating/editing challenges (admin only)"""

    class Meta:
        model = Challenge
        fields = [
            'title', 'slug', 'description', 'short_description', 'cover_image',
            'duration_days', 'difficulty', 'goal_type', 'tracking_type',
            'daily_target', 'daily_requirement', 'points_reward', 'badge_name',
            'badge_icon', 'is_active', 'is_featured', 'max_participants',
            'recommended_for_bmi_range', 'recommended_for_goals'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none',
                'placeholder': 'Challenge Title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none',
                'placeholder': 'challenge-slug'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none',
                'rows': 5,
                'placeholder': 'Detailed description of the challenge...'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none',
                'placeholder': 'Brief summary for challenge cards'
            }),
            'duration_days': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none',
                'min': '1'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none'
            }),
            'goal_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none'
            }),
            'tracking_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none'
            }),
            'daily_target': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none',
                'step': '0.01'
            }),
            'daily_requirement': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none',
                'rows': 3,
                'placeholder': 'e.g., "Walk 10,000 steps daily"'
            }),
            'points_reward': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none'
            }),
            'badge_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none',
                'placeholder': 'e.g., "Hydration Hero"'
            }),
            'badge_icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none',
                'placeholder': 'e.g., 🥇 or 💧'
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none'
            }),
            'recommended_for_bmi_range': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none',
                'placeholder': 'e.g., "25-30"'
            }),
        }


class DailyCheckInForm(forms.ModelForm):
    """Form for daily check-ins"""

    class Meta:
        model = DailyCheckIn
        fields = ['completed', 'value_logged', 'mood', 'difficulty', 'notes']
        widgets = {
            'completed': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'
            }),
            'value_logged': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none',
                'step': '0.01',
                'placeholder': 'Enter value (steps, minutes, etc.)'
            }),
            'mood': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none',
                'rows': 3,
                'placeholder': 'How did it go today? (optional)'
            }),
        }
