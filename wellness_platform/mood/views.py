from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from .models import MoodEntry
from .forms import MoodEntryForm


@login_required
def mood_log(request):
    """Log today's mood"""
    today = date.today()

    # Check if mood already logged today
    existing_entry = MoodEntry.get_today_mood(request.user)

    if request.method == 'POST':
        if existing_entry:
            form = MoodEntryForm(request.POST, instance=existing_entry)
            action = 'updated'
        else:
            form = MoodEntryForm(request.POST)
            action = 'logged'

        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.user = request.user
            mood_entry.entry_date = today
            mood_entry.save()
            messages.success(request, f'Mood {action} successfully!')
            return redirect('mood:mood_history')
    else:
        form = MoodEntryForm(instance=existing_entry) if existing_entry else MoodEntryForm()

    context = {
        'form': form,
        'existing_entry': existing_entry,
        'today': today,
    }
    return render(request, 'mood/mood_log.html', context)


@login_required
def mood_history(request):
    """View mood history"""
    mood_entries = request.user.mood_entries.all()

    context = {
        'mood_entries': mood_entries,
        'total_entries': mood_entries.count(),
        'has_logged_today': MoodEntry.has_logged_today(request.user),
    }
    return render(request, 'mood/mood_history.html', context)


@login_required
def mood_detail(request, pk):
    """View a specific mood entry"""
    mood_entry = get_object_or_404(MoodEntry, pk=pk, user=request.user)

    context = {
        'mood_entry': mood_entry,
    }
    return render(request, 'mood/mood_detail.html', context)


@login_required
def mood_delete(request, pk):
    """Delete a mood entry"""
    mood_entry = get_object_or_404(MoodEntry, pk=pk, user=request.user)

    if request.method == 'POST':
        entry_date = mood_entry.entry_date
        mood_entry.delete()
        messages.success(request, f'Mood entry for {entry_date} deleted successfully!')
        return redirect('mood:mood_history')

    context = {
        'mood_entry': mood_entry,
    }
    return render(request, 'mood/mood_confirm_delete.html', context)
