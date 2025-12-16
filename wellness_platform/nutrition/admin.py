from django.contrib import admin
from .models import Meal, NutritionGoal


@admin.register(NutritionGoal)
class NutritionGoalAdmin(admin.ModelAdmin):
    """Admin interface for nutrition goals"""
    list_display = ['user', 'calorie_goal', 'protein_goal', 'carbs_goal', 'fat_goal', 'updated_at']
    search_fields = ['user__username', 'user__email']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Daily Goals', {
            'fields': ('calorie_goal', 'protein_goal', 'carbs_goal', 'fat_goal')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    """Admin interface for meal entries"""
    list_display = ['user', 'meal_type', 'food_name', 'calories', 'meal_date', 'logged_at']
    list_filter = ['meal_type', 'meal_date', 'logged_at']
    search_fields = ['user__username', 'food_name', 'notes']
    date_hierarchy = 'meal_date'
    readonly_fields = ['logged_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'meal_type', 'food_name', 'portion', 'meal_date')
        }),
        ('Nutritional Information', {
            'fields': ('calories', 'protein', 'carbs', 'fat')
        }),
        ('Additional Details', {
            'fields': ('notes', 'logged_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user')
