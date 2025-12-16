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
    
    # Get habits data
    active_habits = request.user.habits.filter(is_active=True)
    habits_completed_today = sum(1 for habit in active_habits if habit.is_completed_today())
    total_active_habits = active_habits.count()
    
    # Calculate current streak (sum of all active habit streaks)
    current_streak = sum(habit.current_streak for habit in active_habits)
    
    # Get today's mood
    today_mood = MoodEntry.get_today_mood(request.user)
    
    context = {
        'user': request.user,
        'habits_completed_today': habits_completed_today,
        'total_active_habits': total_active_habits,
        'current_streak': current_streak,
        'today_mood': today_mood,
        'has_logged_mood_today': today_mood is not None,
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
