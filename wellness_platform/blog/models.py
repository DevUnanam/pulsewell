from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
import markdown


class Article(models.Model):
    """
    Blog article model - only admin/superuser can create
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(help_text="Write your article content in Markdown format")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    video = models.FileField(upload_to='blog/videos/', blank=True, null=True)
    likes_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})

    def get_content_html(self):
        """Convert markdown content to HTML"""
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.tables',
                'markdown.extensions.nl2br',
                'markdown.extensions.sane_lists',
            ],
            output_format='html5'
        )
        return md.convert(self.content)

    def get_content_preview(self, max_length=200):
        """Get plain text preview of content"""
        # Strip markdown formatting
        text = self.content.replace('#', '').replace('*', '').replace('_', '')
        text = ' '.join(text.split())
        if len(text) > max_length:
            return text[:max_length] + '...'
        return text

    def update_comment_count(self):
        """Update comment count for this article"""
        self.comment_count = self.comments.count()
        self.save(update_fields=['comment_count'])

    def get_reading_time(self):
        """Calculate estimated reading time in minutes"""
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))


class Comment(models.Model):
    """
    Comment model - supports nested replies
    """
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_comments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    content = models.TextField(max_length=1000)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_comments',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['article', 'created_at']),
        ]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"

    def get_likes_count(self):
        """Get total likes for this comment"""
        return self.likes.count()

    def is_reply(self):
        """Check if this comment is a reply to another comment"""
        return self.parent is not None

    def get_replies(self):
        """Get all replies to this comment"""
        return self.replies.all()

    def save(self, *args, **kwargs):
        """Update article comment count after saving"""
        super().save(*args, **kwargs)
        self.article.update_comment_count()

    def delete(self, *args, **kwargs):
        """Update article comment count after deletion"""
        article = self.article
        super().delete(*args, **kwargs)
        article.update_comment_count()
