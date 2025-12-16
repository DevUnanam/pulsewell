from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]

    UNIT_CHOICES = [
        ('metric', 'Metric (kg, cm)'),
        ('imperial', 'Imperial (lbs, inches)'),
    ]

    # Core relationship
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    # Profile Picture
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, help_text='Upload your profile picture')

    # Personal Information
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text='Your contact number')
    date_of_birth = models.DateField(null=True, blank=True, help_text='Your date of birth')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    # Address Information
    address_line1 = models.CharField(max_length=255, blank=True, null=True, help_text='Street address')
    address_line2 = models.CharField(max_length=255, blank=True, null=True, help_text='Apartment, suite, etc.')
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True, help_text='State/Province')
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Health & Wellness Information
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Height in feet (e.g., 5.8 for 5\'8")')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Weight in kilograms (kg)')
    unit_preference = models.CharField(max_length=10, choices=UNIT_CHOICES, default='metric')

    # Wellness Details
    bio = models.TextField(blank=True, null=True, help_text='Tell us about yourself and your wellness journey')
    wellness_goals = models.TextField(blank=True, null=True, help_text='Your wellness goals')
    medical_conditions = models.TextField(blank=True, null=True, help_text='Any medical conditions (optional)')
    allergies = models.TextField(blank=True, null=True, help_text='Any allergies (optional)')

    # Interests & Tags
    interests = models.ManyToManyField('profiles.Tag', blank=True, related_name='user_profiles')

    # Privacy Settings
    profile_visibility = models.BooleanField(default=True, help_text='Make your profile visible to others')
    show_email = models.BooleanField(default=False, help_text='Show email on public profile')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_age(self):
        """Calculate user's age from date of birth"""
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    def get_bmi(self):
        """Calculate BMI (Body Mass Index)
        Height is stored in feet, weight in kg
        """
        if self.height and self.weight:
            # Convert feet to meters (1 foot = 0.3048 meters)
            height_m = float(self.height) * 0.3048
            # BMI = weight(kg) / (height(m))^2
            return round(float(self.weight) / (height_m ** 2), 2)
        return None

    def get_bmi_category(self):
        """Get BMI category based on calculated BMI"""
        bmi = self.get_bmi()
        if bmi:
            if bmi < 18.5:
                return 'UNDERWEIGHT'
            elif bmi < 25:
                return 'HEALTHY WEIGHT'
            elif bmi < 30:
                return 'OVERWEIGHT'
            else:
                return 'OBESE'
        return None


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return self.name


# Signal to automatically create profile when user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)