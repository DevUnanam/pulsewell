from django import forms
from .models import Meal, NutritionGoal


class MealForm(forms.ModelForm):
    """Form for logging meals"""

    class Meta:
        model = Meal
        fields = ['meal_type', 'food_name', 'portion', 'calories', 'protein', 'carbs', 'fat', 'meal_date', 'notes']
        widgets = {
            'meal_type': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'food_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'e.g., Grilled chicken breast, Oatmeal with berries'
            }),
            'portion': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'e.g., 1 cup, 150g, 2 slices'
            }),
            'calories': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': '0'
            }),
            'protein': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': '0',
                'step': '0.1'
            }),
            'carbs': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': '0',
                'step': '0.1'
            }),
            'fat': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': '0',
                'step': '0.1'
            }),
            'meal_date': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'rows': 3,
                'placeholder': 'Optional notes about this meal...'
            }),
        }
        labels = {
            'meal_type': 'Meal Type',
            'food_name': 'Food Name',
            'portion': 'Portion/Quantity',
            'calories': 'Calories (kcal)',
            'protein': 'Protein (g)',
            'carbs': 'Carbs (g)',
            'fat': 'Fat (g)',
            'meal_date': 'Date',
            'notes': 'Notes (Optional)'
        }


class NutritionGoalForm(forms.ModelForm):
    """Form for setting nutrition goals"""

    class Meta:
        model = NutritionGoal
        fields = ['calorie_goal', 'protein_goal', 'carbs_goal', 'fat_goal']
        widgets = {
            'calorie_goal': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'min': '0',
                'placeholder': '2000'
            }),
            'protein_goal': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'min': '0',
                'placeholder': '50'
            }),
            'carbs_goal': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'min': '0',
                'placeholder': '250'
            }),
            'fat_goal': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'min': '0',
                'placeholder': '70'
            }),
        }
        labels = {
            'calorie_goal': 'Daily Calorie Goal (kcal)',
            'protein_goal': 'Daily Protein Goal (g)',
            'carbs_goal': 'Daily Carbs Goal (g)',
            'fat_goal': 'Daily Fat Goal (g)',
        }
        help_texts = {
            'calorie_goal': 'Recommended: 1500-2500 kcal per day',
            'protein_goal': 'Recommended: 50-150g per day',
            'carbs_goal': 'Recommended: 200-300g per day',
            'fat_goal': 'Recommended: 50-100g per day',
        }
