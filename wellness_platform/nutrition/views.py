from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta
from .models import Meal, NutritionGoal
from .forms import MealForm, NutritionGoalForm


@login_required
def meal_log(request):
    """Log a new meal"""
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, f'✅ {meal.get_meal_type_display()} logged successfully!')
            return redirect('nutrition:daily_summary')
    else:
        # Pre-fill with today's date
        form = MealForm(initial={'meal_date': date.today()})
    
    return render(request, 'nutrition/meal_log.html', {'form': form})


@login_required
def meal_edit(request, pk):
    """Edit an existing meal"""
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ {meal.get_meal_type_display()} updated successfully!')
            return redirect('nutrition:daily_summary')
    else:
        form = MealForm(instance=meal)
    
    return render(request, 'nutrition/meal_form.html', {
        'form': form,
        'meal': meal,
        'is_edit': True
    })


@login_required
def meal_delete(request, pk):
    """Delete a meal"""
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        meal_type = meal.get_meal_type_display()
        meal.delete()
        messages.success(request, f'🗑️ {meal_type} deleted successfully!')
        return redirect('nutrition:daily_summary')
    
    return render(request, 'nutrition/meal_confirm_delete.html', {'meal': meal})


@login_required
def daily_summary(request):
    """View daily nutrition summary"""
    # Get selected date from query params or use today
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = date.fromisoformat(selected_date_str)
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()
    
    # Get daily summary
    summary = Meal.get_daily_summary(request.user, selected_date)
    
    # Get user's nutrition goals if they exist
    try:
        nutrition_goal = request.user.nutrition_goal
        progress = nutrition_goal.get_daily_progress(selected_date)
    except NutritionGoal.DoesNotExist:
        nutrition_goal = None
        progress = None
    
    # Calculate previous and next dates for navigation
    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)
    
    context = {
        'summary': summary,
        'nutrition_goal': nutrition_goal,
        'progress': progress,
        'selected_date': selected_date,
        'prev_date': prev_date,
        'next_date': next_date,
        'is_today': selected_date == date.today(),
    }
    
    return render(request, 'nutrition/daily_summary.html', context)


@login_required
def weekly_summary(request):
    """View weekly nutrition summary and analytics"""
    # Get selected end date from query params or use today
    end_date_str = request.GET.get('date')
    if end_date_str:
        try:
            end_date = date.fromisoformat(end_date_str)
        except ValueError:
            end_date = date.today()
    else:
        end_date = date.today()
    
    # Get weekly summary
    summary = Meal.get_weekly_summary(request.user, end_date)
    
    # Get user's nutrition goals if they exist
    try:
        nutrition_goal = request.user.nutrition_goal
    except NutritionGoal.DoesNotExist:
        nutrition_goal = None
    
    # Calculate previous and next week dates for navigation
    prev_week_end = end_date - timedelta(days=7)
    next_week_end = end_date + timedelta(days=7)
    
    # Get daily data for the week for visualization
    daily_data = []
    for i in range(7):
        day_date = summary['start_date'] + timedelta(days=i)
        day_summary = Meal.get_daily_summary(request.user, day_date)
        daily_data.append({
            'date': day_date,
            'calories': day_summary['total_calories'],
            'protein': day_summary['total_protein'],
            'carbs': day_summary['total_carbs'],
            'fat': day_summary['total_fat'],
            'meal_count': day_summary['meal_count'],
        })
    
    context = {
        'summary': summary,
        'nutrition_goal': nutrition_goal,
        'daily_data': daily_data,
        'end_date': end_date,
        'prev_week_end': prev_week_end,
        'next_week_end': next_week_end,
        'is_current_week': end_date == date.today(),
    }
    
    return render(request, 'nutrition/weekly_summary.html', context)


@login_required
def nutrition_goals(request):
    """View and edit nutrition goals"""
    try:
        goal = request.user.nutrition_goal
    except NutritionGoal.DoesNotExist:
        goal = None
    
    if request.method == 'POST':
        if goal:
            form = NutritionGoalForm(request.POST, instance=goal)
        else:
            form = NutritionGoalForm(request.POST)
        
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, '🎯 Nutrition goals updated successfully!')
            return redirect('nutrition:daily_summary')
    else:
        form = NutritionGoalForm(instance=goal)
    
    return render(request, 'nutrition/nutrition_goals.html', {
        'form': form,
        'goal': goal
    })


@login_required
def meal_history(request):
    """View complete meal history"""
    meals = Meal.objects.filter(user=request.user).select_related('user')
    
    # Filter by meal type if provided
    meal_type_filter = request.GET.get('meal_type')
    if meal_type_filter and meal_type_filter in dict(Meal.MEAL_TYPE_CHOICES):
        meals = meals.filter(meal_type=meal_type_filter)
    
    # Get statistics
    total_meals = meals.count()
    
    context = {
        'meals': meals[:50],  # Limit to recent 50 meals
        'total_meals': total_meals,
        'meal_type_filter': meal_type_filter,
        'meal_types': Meal.MEAL_TYPE_CHOICES,
    }
    
    return render(request, 'nutrition/meal_history.html', context)
