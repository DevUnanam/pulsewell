from django import forms
from .models import MoodEntry


class MoodEntryForm(forms.ModelForm):
    """Form for creating and editing mood entries"""
    
    class Meta:
        model = MoodEntry
        fields = ['mood', 'note']
        widgets = {
            'mood': forms.RadioSelect(attrs={
                'class': 'mood-radio'
            }),
            'note': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white',
                'placeholder': 'How are you feeling? (Optional)',
                'rows': 3
            }),
        }
        labels = {
            'mood': 'How are you feeling today?',
            'note': 'Add a note (Optional)',
        }
