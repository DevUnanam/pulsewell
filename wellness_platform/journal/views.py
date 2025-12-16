from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import JournalEntry
from .forms import JournalEntryForm


@login_required
def journal_list(request):
    """Display list of user's journal entries"""
    entries = JournalEntry.objects.filter(user=request.user)

    # Get statistics
    total_entries = entries.count()
    total_words = sum(entry.get_word_count() for entry in entries)

    context = {
        'entries': entries,
        'total_entries': total_entries,
        'total_words': total_words,
    }
    return render(request, 'journal/journal_list.html', context)


@login_required
def journal_create(request):
    """Create a new journal entry"""
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, f'✍️ Journal entry "{entry.title}" created successfully!')
            return redirect('journal:journal_detail', pk=entry.pk)
    else:
        form = JournalEntryForm()

    return render(request, 'journal/journal_form.html', {
        'form': form,
        'is_edit': False
    })


@login_required
def journal_detail(request, pk):
    """View a single journal entry"""
    entry = get_object_or_404(JournalEntry, pk=pk)

    # Security: Only owner can view their entries
    if entry.user != request.user:
        return HttpResponseForbidden("You don't have permission to view this entry.")

    context = {
        'entry': entry,
        'content_html': entry.get_content_html(),
    }
    return render(request, 'journal/journal_detail.html', context)


@login_required
def journal_edit(request, pk):
    """Edit an existing journal entry"""
    entry = get_object_or_404(JournalEntry, pk=pk)

    # Security: Only owner can edit their entries
    if entry.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this entry.")

    if request.method == 'POST':
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Journal entry "{entry.title}" updated successfully!')
            return redirect('journal:journal_detail', pk=entry.pk)
    else:
        form = JournalEntryForm(instance=entry)

    return render(request, 'journal/journal_form.html', {
        'form': form,
        'entry': entry,
        'is_edit': True
    })


@login_required
def journal_delete(request, pk):
    """Delete a journal entry"""
    entry = get_object_or_404(JournalEntry, pk=pk)

    # Security: Only owner can delete their entries
    if entry.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this entry.")

    if request.method == 'POST':
        title = entry.title
        entry.delete()
        messages.success(request, f'🗑️ Journal entry "{title}" deleted successfully!')
        return redirect('journal:journal_list')

    return render(request, 'journal/journal_confirm_delete.html', {'entry': entry})
