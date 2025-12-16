from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import date


def is_admin_user(user):
    """Check if user is admin or superuser"""
    return user.is_superuser or user.is_admin


def is_regular_user(user):
    """Check if user is a regular user (not admin)"""
    return not (user.is_superuser or user.is_admin)


@login_required
@user_passes_test(is_regular_user, login_url='/dashboard/admin/')
def user_dashboard_view(request):
    """
    Display the main dashboard for regular users only
    """
    # Import models here to avoid circular imports
    from habits.models import Habit
    from mood.models import MoodEntry
    from nutrition.models import Meal, NutritionGoal
    from journal.models import JournalEntry

    # Get habits data
    active_habits = request.user.habits.filter(is_active=True)
    habits_completed_today = sum(1 for habit in active_habits if habit.is_completed_today())
    total_active_habits = active_habits.count()

    # Calculate current streak (sum of all active habit streaks)
    current_streak = sum(habit.current_streak for habit in active_habits)

    # Get today's mood
    today_mood = MoodEntry.get_today_mood(request.user)

    # Get nutrition data for today
    nutrition_summary = Meal.get_daily_summary(request.user, date.today())

    # Get nutrition goal if exists
    try:
        nutrition_goal = request.user.nutrition_goal
    except NutritionGoal.DoesNotExist:
        nutrition_goal = None

    # Get journal statistics
    user_journal_entries = JournalEntry.objects.filter(user=request.user)
    total_journal_entries = user_journal_entries.count()
    total_journal_words = sum(entry.get_word_count() for entry in user_journal_entries)
    recent_journal_entries = user_journal_entries[:3]

    if total_journal_entries > 0:
        avg_journal_words = total_journal_words // total_journal_entries
    else:
        avg_journal_words = 0

    context = {
        'user': request.user,
        'habits_completed_today': habits_completed_today,
        'total_active_habits': total_active_habits,
        'current_streak': current_streak,
        'today_mood': today_mood,
        'has_logged_mood_today': today_mood is not None,
        'nutrition_summary': nutrition_summary,
        'nutrition_goal': nutrition_goal,
        'total_journal_entries': total_journal_entries,
        'total_journal_words': total_journal_words,
        'recent_journal_entries': recent_journal_entries,
        'avg_journal_words': round(avg_journal_words),
    }
    return render(request, 'dashboard/user_dashboard.html', context)


@login_required
@user_passes_test(is_admin_user, login_url='/dashboard/')
def admin_dashboard_view(request):
    """
    Display the admin dashboard - only accessible to superusers and admins
    """
    if not (request.user.is_superuser or request.user.is_admin):
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('dashboard:user_dashboard')

    # Get statistics for admin view
    from django.contrib.auth import get_user_model
    User = get_user_model()

    total_users = User.objects.count()
    admin_users = User.objects.filter(is_admin=True).count()
    regular_users = User.objects.filter(is_user=True, is_admin=False, is_superuser=False).count()

    context = {
        'user': request.user,
        'total_users': total_users,
        'admin_users': admin_users,
        'regular_users': regular_users,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def dashboard_redirect_view(request):
    """
    Redirect to appropriate dashboard based on user role
    """
    if request.user.is_superuser or request.user.is_admin:
        return redirect('dashboard:admin_dashboard')
    return redirect('dashboard:user_dashboard')
