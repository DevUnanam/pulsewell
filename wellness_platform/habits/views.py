from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date, timedelta
from .models import Habit, HabitCompletion
from .forms import HabitForm


@login_required
def habit_list(request):
    """Display all habits for the logged-in user"""
    habits = request.user.habits.filter(is_active=True)

    # Calculate statistics
    total_habits = habits.count()
    completed_today = sum(1 for habit in habits if habit.is_completed_today())
    total_completions = sum(habit.total_completions for habit in habits)
    active_streaks = sum(habit.current_streak for habit in habits)

    context = {
        'habits': habits,
        'total_habits': total_habits,
        'completed_today': completed_today,
        'total_completions': total_completions,
        'active_streaks': active_streaks,
        'today': date.today(),
    }
    return render(request, 'habits/habit_list.html', context)


@login_required
def habit_create(request):
    """Create a new habit"""
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            try:
                habit.save()
                messages.success(request, f'Habit "{habit.name}" created successfully!')
                return redirect('habits:habit_list')
            except Exception as e:
                messages.error(request, f'Error creating habit: {str(e)}')
    else:
        form = HabitForm()

    context = {
        'form': form,
        'title': 'Create New Habit',
    }
    return render(request, 'habits/habit_form.html', context)


@login_required
def habit_detail(request, pk):
    """Display detailed view of a specific habit"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)

    # Get completion history for the last 30 days
    end_date = date.today()
    start_date = end_date - timedelta(days=29)

    completions = habit.completions.filter(
        completed_date__gte=start_date,
        completed_date__lte=end_date
    ).values_list('completed_date', flat=True)

    # Create calendar data
    calendar_data = []
    current_date = start_date
    while current_date <= end_date:
        calendar_data.append({
            'date': current_date,
            'completed': current_date in completions,
            'is_today': current_date == end_date,
        })
        current_date += timedelta(days=1)

    # Get completion rate
    completion_rate = habit.get_completion_rate(days=30)

    context = {
        'habit': habit,
        'calendar_data': calendar_data,
        'completion_rate': completion_rate,
        'can_complete': habit.can_complete_today(),
    }
    return render(request, 'habits/habit_detail.html', context)


@login_required
def habit_edit(request, pk):
    """Edit an existing habit"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)

    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, f'Habit "{habit.name}" updated successfully!')
            return redirect('habits:habit_detail', pk=habit.pk)
    else:
        form = HabitForm(instance=habit)

    context = {
        'form': form,
        'habit': habit,
        'title': f'Edit {habit.name}',
    }
    return render(request, 'habits/habit_form.html', context)


@login_required
def habit_delete(request, pk):
    """Delete a habit"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)

    if request.method == 'POST':
        habit_name = habit.name
        habit.delete()
        messages.success(request, f'Habit "{habit_name}" deleted successfully!')
        return redirect('habits:habit_list')

    context = {
        'habit': habit,
    }
    return render(request, 'habits/habit_confirm_delete.html', context)


@login_required
def habit_complete(request, pk):
    """Mark a habit as complete for today"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)

    if request.method == 'POST':
        success, message = habit.mark_complete()
        if success:
            messages.success(request, message)
        else:
            messages.warning(request, message)

    # Redirect back to the referring page or habit list
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', 'habits:habit_list'))
    if next_url and next_url.startswith('/'):
        return redirect(next_url)
    return redirect('habits:habit_list')


@login_required
def habit_uncomplete(request, pk):
    """Remove today's completion for a habit"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)

    if request.method == 'POST':
        today = date.today()
        try:
            completion = habit.completions.get(completed_date=today)
            completion.delete()

            # Update streaks and total
            habit.update_streaks()
            habit.total_completions = max(0, habit.total_completions - 1)
            habit.save()

            messages.success(request, f'Completion removed for "{habit.name}"')
        except HabitCompletion.DoesNotExist:
            messages.warning(request, 'Habit was not completed today')

    # Redirect back to the referring page or habit list
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', 'habits:habit_list'))
    if next_url and next_url.startswith('/'):
        return redirect(next_url)
    return redirect('habits:habit_list')


@login_required
def habit_toggle_active(request, pk):
    """Toggle habit active status"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)

    if request.method == 'POST':
        habit.is_active = not habit.is_active
        habit.save()
        status = 'activated' if habit.is_active else 'deactivated'
        messages.success(request, f'Habit "{habit.name}" {status}')

    return redirect('habits:habit_detail', pk=habit.pk)
