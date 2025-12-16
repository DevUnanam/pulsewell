from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    """
    Form for creating and editing articles (admin only)
    """
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'video', 'published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                'placeholder': 'Enter article title...',
                'autofocus': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white font-mono focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                'rows': 25,
                'placeholder': '# Write your article in Markdown\n\n## Subheading\n\nYour content here...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-900 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg cursor-pointer bg-gray-50 dark:bg-gray-700 focus:outline-none',
                'accept': 'image/*'
            }),
            'video': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-900 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg cursor-pointer bg-gray-50 dark:bg-gray-700 focus:outline-none',
                'accept': 'video/*'
            }),
            'published': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-indigo-600 bg-gray-100 border-gray-300 rounded focus:ring-indigo-500 dark:focus:ring-indigo-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
            })
        }
        help_texts = {
            'content': 'Use Markdown syntax to format your article',
            'image': 'Optional: Upload a featured image for this article',
            'video': 'Optional: Upload a video for this article',
            'published': 'Uncheck to save as draft'
        }


class CommentForm(forms.ModelForm):
    """
    Form for posting comments and replies
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none',
                'rows': 4,
                'placeholder': 'Share your thoughts...',
                'maxlength': '1000'
            })
        }
        labels = {
            'content': ''
        }

    def __init__(self, *args, **kwargs):
        is_reply = kwargs.pop('is_reply', False)
        super().__init__(*args, **kwargs)
        if is_reply:
            self.fields['content'].widget.attrs['placeholder'] = 'Write your reply...'
            self.fields['content'].widget.attrs['rows'] = 3
