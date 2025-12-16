from django import forms
from .models import JournalEntry


class JournalEntryForm(forms.ModelForm):
    """Form for creating and editing journal entries"""

    class Meta:
        model = JournalEntry
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-lg',
                'placeholder': 'Entry title...',
                'autofocus': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500 font-mono',
                'rows': 20,
                'placeholder': '# Start writing...\n\nUse **Markdown** to format your entry.\n\n## You can use:\n- Headings\n- **Bold** and *italic* text\n- Lists\n- > Blockquotes\n- Code blocks\n- And more!',
                'id': 'markdown-editor'
            }),
        }
        labels = {
            'title': 'Title',
            'content': 'Content (Markdown supported)',
        }
        help_texts = {
            'title': 'Give your journal entry a meaningful title',
            'content': 'Write your thoughts using Markdown formatting',
        }
