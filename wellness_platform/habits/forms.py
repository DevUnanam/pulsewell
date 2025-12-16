from django import forms
from .models import Habit


class HabitForm(forms.ModelForm):
    """Form for creating and editing habits"""

    class Meta:
        model = Habit
        fields = ['name', 'description', 'frequency', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white',
                'placeholder': 'e.g., Morning meditation'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white',
                'placeholder': 'Optional: Describe your habit...',
                'rows': 3
            }),
            'frequency': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white'
            }),
        }
        labels = {
            'name': 'Habit Name',
            'description': 'Description (Optional)',
            'frequency': 'Frequency',
            'category': 'Category (Optional)',
        }
