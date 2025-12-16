from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Sum


class NutritionGoal(models.Model):
    """Model for user's daily nutrition goals"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='nutrition_goal'
    )
    calorie_goal = models.PositiveIntegerField(default=2000, help_text="Daily calorie target")
    protein_goal = models.PositiveIntegerField(default=50, help_text="Daily protein target (grams)")
    carbs_goal = models.PositiveIntegerField(default=250, help_text="Daily carbs target (grams)")
    fat_goal = models.PositiveIntegerField(default=70, help_text="Daily fat target (grams)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Nutrition Goal"
        verbose_name_plural = "Nutrition Goals"

    def __str__(self):
        return f"{self.user.username}'s Nutrition Goals"

    def get_daily_progress(self, target_date=None):
        """Calculate progress towards goals for a specific date"""
        if target_date is None:
            target_date = date.today()

        meals = Meal.objects.filter(user=self.user, meal_date=target_date)
        totals = meals.aggregate(
            total_calories=Sum('calories'),
            total_protein=Sum('protein'),
            total_carbs=Sum('carbs'),
            total_fat=Sum('fat')
        )

        return {
            'calories': {
                'consumed': totals['total_calories'] or 0,
                'goal': self.calorie_goal,
                'percentage': min(100, round((totals['total_calories'] or 0) / self.calorie_goal * 100, 1)) if self.calorie_goal > 0 else 0
            },
            'protein': {
                'consumed': totals['total_protein'] or 0,
                'goal': self.protein_goal,
                'percentage': min(100, round((totals['total_protein'] or 0) / self.protein_goal * 100, 1)) if self.protein_goal > 0 else 0
            },
            'carbs': {
                'consumed': totals['total_carbs'] or 0,
                'goal': self.carbs_goal,
                'percentage': min(100, round((totals['total_carbs'] or 0) / self.carbs_goal * 100, 1)) if self.carbs_goal > 0 else 0
            },
            'fat': {
                'consumed': totals['total_fat'] or 0,
                'goal': self.fat_goal,
                'percentage': min(100, round((totals['total_fat'] or 0) / self.fat_goal * 100, 1)) if self.fat_goal > 0 else 0
            }
        }


class Meal(models.Model):
    """Model for logging individual meals"""
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='meals'
    )
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    food_name = models.CharField(max_length=200, help_text="Name or description of the food")
    portion = models.CharField(max_length=100, help_text="e.g., 1 cup, 100g, 2 slices")

    # Nutritional information
    calories = models.PositiveIntegerField(help_text="Calories (kcal)")
    protein = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        default=0,
        help_text="Protein in grams"
    )
    carbs = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        default=0,
        help_text="Carbohydrates in grams"
    )
    fat = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        default=0,
        help_text="Fat in grams"
    )

    # Metadata
    meal_date = models.DateField(default=date.today)
    logged_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Optional notes about the meal")

    class Meta:
        verbose_name = "Meal"
        verbose_name_plural = "Meals"
        ordering = ['-meal_date', '-logged_at']
        indexes = [
            models.Index(fields=['user', 'meal_date']),
            models.Index(fields=['meal_date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.get_meal_type_display()} - {self.food_name} ({self.meal_date})"

    @classmethod
    def get_daily_summary(cls, user, target_date=None):
        """Get nutrition summary for a specific date"""
        if target_date is None:
            target_date = date.today()

        meals = cls.objects.filter(user=user, meal_date=target_date)
        totals = meals.aggregate(
            total_calories=Sum('calories'),
            total_protein=Sum('protein'),
            total_carbs=Sum('carbs'),
            total_fat=Sum('fat')
        )

        return {
            'date': target_date,
            'meal_count': meals.count(),
            'total_calories': totals['total_calories'] or 0,
            'total_protein': totals['total_protein'] or 0,
            'total_carbs': totals['total_carbs'] or 0,
            'total_fat': totals['total_fat'] or 0,
            'meals': meals
        }

    @classmethod
    def get_weekly_summary(cls, user, target_date=None):
        """Get nutrition summary for the past 7 days"""
        if target_date is None:
            target_date = date.today()

        start_date = target_date - timedelta(days=6)
        meals = cls.objects.filter(
            user=user,
            meal_date__gte=start_date,
            meal_date__lte=target_date
        )

        totals = meals.aggregate(
            total_calories=Sum('calories'),
            total_protein=Sum('protein'),
            total_carbs=Sum('carbs'),
            total_fat=Sum('fat')
        )

        meal_type_counts = {}
        for meal_type, _ in cls.MEAL_TYPE_CHOICES:
            meal_type_counts[meal_type] = meals.filter(meal_type=meal_type).count()

        most_frequent_meal = max(meal_type_counts.items(), key=lambda x: x[1])[0] if meals.exists() else None

        return {
            'start_date': start_date,
            'end_date': target_date,
            'total_meals': meals.count(),
            'avg_calories_per_day': round((totals['total_calories'] or 0) / 7, 1),
            'avg_protein_per_day': round((totals['total_protein'] or 0) / 7, 1),
            'avg_carbs_per_day': round((totals['total_carbs'] or 0) / 7, 1),
            'avg_fat_per_day': round((totals['total_fat'] or 0) / 7, 1),
            'most_frequent_meal_type': most_frequent_meal,
            'meal_type_counts': meal_type_counts
        }

    def get_meal_type_emoji(self):
        """Return emoji for meal type"""
        emoji_map = {
            'breakfast': '🍳',
            'lunch': '🍽️',
            'dinner': '🍲',
            'snack': '🍎'
        }
        return emoji_map.get(self.meal_type, '🍴')
