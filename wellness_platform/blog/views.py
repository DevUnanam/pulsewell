from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from .models import Article, Comment
from .forms import ArticleForm, CommentForm


def is_admin_user(user):
    """Check if user is admin or superuser"""
    return user.is_superuser or user.is_admin


def article_list(request):
    """
    Display list of all published articles
    Available to all users (authenticated and anonymous)
    """
    articles = Article.objects.filter(published=True).select_related('author')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    context = {
        'articles': articles,
        'search_query': search_query,
    }
    return render(request, 'blog/article_list.html', context)


def article_detail(request, slug):
    """
    Display single article with comments
    Available to all users
    """
    article = get_object_or_404(
        Article.objects.select_related('author'),
        slug=slug,
        published=True
    )
    
    # Get all comments (only top-level, replies are nested)
    comments = article.comments.filter(parent=None).select_related('user').prefetch_related('replies__user')
    
    # Comment form for logged-in users
    comment_form = CommentForm() if request.user.is_authenticated else None
    
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'content_html': article.get_content_html(),
    }
    return render(request, 'blog/article_detail.html', context)


@login_required
@require_POST
def post_comment(request, slug):
    """
    Post a new comment on an article
    Requires authentication
    """
    article = get_object_or_404(Article, slug=slug, published=True)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = request.user
        
        # Check if this is a reply
        parent_id = request.POST.get('parent_id')
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id, article=article)
            comment.parent = parent_comment
        
        comment.save()
        messages.success(request, 'Comment posted successfully!')
    else:
        messages.error(request, 'Error posting comment. Please try again.')
    
    return redirect('blog:article_detail', slug=slug)


@login_required
@require_POST
def delete_comment(request, comment_id):
    """
    Delete a comment
    Users can only delete their own comments
    Admins can delete any comment
    """
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check permissions
    if comment.user == request.user or is_admin_user(request.user):
        article_slug = comment.article.slug
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('blog:article_detail', slug=article_slug)
    else:
        return HttpResponseForbidden("You don't have permission to delete this comment.")


@login_required
@require_POST
def like_comment(request, comment_id):
    """
    Like or unlike a comment
    Returns JSON response for AJAX
    """
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user in comment.likes.all():
        # Unlike
        comment.likes.remove(request.user)
        liked = False
    else:
        # Like
        comment.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': comment.get_likes_count()
    })


@login_required
@user_passes_test(is_admin_user)
def create_article(request):
    """
    Create a new article
    Admin only
    """
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, f'Article "{article.title}" created successfully!')
            return redirect('blog:article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    return render(request, 'blog/article_form.html', context)


@login_required
@user_passes_test(is_admin_user)
def edit_article(request, slug):
    """
    Edit an existing article
    Admin only
    """
    article = get_object_or_404(Article, slug=slug)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, f'Article "{article.title}" updated successfully!')
            return redirect('blog:article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    
    context = {
        'form': form,
        'article': article,
        'action': 'Edit',
    }
    return render(request, 'blog/article_form.html', context)


@login_required
@user_passes_test(is_admin_user)
def delete_article(request, slug):
    """
    Delete an article
    Admin only
    """
    article = get_object_or_404(Article, slug=slug)
    
    if request.method == 'POST':
        title = article.title
        article.delete()
        messages.success(request, f'Article "{title}" deleted successfully!')
        return redirect('blog:article_list')
    
    context = {
        'article': article,
    }
    return render(request, 'blog/article_confirm_delete.html', context)
