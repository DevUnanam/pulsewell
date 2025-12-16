from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    """Form for updating user basic information"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'placeholder': 'Email address'
        })
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'placeholder': 'Last name'
        })
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile information"""

    # Personal Information
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'placeholder': '+1 234 567 8900'
        })
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'type': 'date'
        })
    )
    gender = forms.ChoiceField(
        required=False,
        choices=[('', 'Select gender')] + list(UserProfile.GENDER_CHOICES),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200'
        })
    )

    # Address
    address_line1 = forms.CharField(
        required=False,
        label='Address Line 1',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'placeholder': 'Street address'
        })
    )
    address_line2 = forms.CharField(
        required=False,
        label='Address Line 2',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'placeholder': 'Apartment, suite, etc.'
        })
    )
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'placeholder': 'City'
        })
    )
    state = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'placeholder': 'State/Province'
        })
    )
    postal_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'placeholder': 'Postal/ZIP code'
        })
    )
    country = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'placeholder': 'Country'
        })
    )

    # Health Information
    height = forms.DecimalField(
        required=False,
        label='Height (feet)',
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'placeholder': 'e.g., 5.8',
            'step': '0.01',
            'id': 'id_height',
            'oninput': 'calculateBMI()'
        })
    )
    weight = forms.DecimalField(
        required=False,
        label='Weight (kg)',
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'placeholder': 'e.g., 70',
            'step': '0.01',
            'id': 'id_weight',
            'oninput': 'calculateBMI()'
        })
    )

    # Wellness
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'rows': 4,
            'placeholder': 'Tell us about yourself and your wellness journey...'
        })
    )
    wellness_goals = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'rows': 3,
            'placeholder': 'What are your wellness goals?'
        })
    )
    medical_conditions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'rows': 2,
            'placeholder': 'Any medical conditions (optional, kept private)'
        })
    )
    allergies = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'rows': 2,
            'placeholder': 'Any allergies (optional, kept private)'
        })
    )

    # Profile Picture
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-200',
            'accept': 'image/*'
        })
    )

    # Privacy
    profile_visibility = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded cursor-pointer'
        })
    )
    show_email = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded cursor-pointer'
        })
    )

    class Meta:
        model = UserProfile
        fields = [
            'profile_picture', 'phone_number', 'date_of_birth', 'gender',
            'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country',
            'height', 'weight',
            'bio', 'wellness_goals', 'medical_conditions', 'allergies',
            'profile_visibility', 'show_email'
        ]


class AccountDeleteForm(forms.Form):
    """Form for account deletion confirmation"""
    confirm_deletion = forms.BooleanField(
        required=True,
        label='I understand that this action cannot be undone',
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded cursor-pointer'
        })
    )
    password = forms.CharField(
        required=True,
        label='Enter your password to confirm',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 focus:border-red-500 focus:ring-2 focus:ring-red-500 focus:outline-none transition duration-200',
            'placeholder': 'Enter your password'
        })
    )
