from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Article URLs
    path('', views.article_list, name='article_list'),
    path('create/', views.create_article, name='create_article'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
    path('<slug:slug>/edit/', views.edit_article, name='edit_article'),
    path('<slug:slug>/delete/', views.delete_article, name='delete_article'),

    # Comment URLs
    path('<slug:slug>/comment/', views.post_comment, name='post_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
]
