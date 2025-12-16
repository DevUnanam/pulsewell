from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
    # Public/User Views
    path('', views.challenge_explore, name='explore'),
    path('my-challenges/', views.my_challenges, name='my_challenges'),
    path('recommended/', views.recommended_challenges, name='recommended'),
    path('<slug:slug>/', views.challenge_detail, name='detail'),
    path('<slug:slug>/join/', views.challenge_join, name='join'),
    path('my/<int:pk>/', views.my_challenge_detail, name='my_challenge'),
    path('my/<int:pk>/checkin/', views.daily_checkin, name='daily_checkin'),

    # Admin-only Views
    path('admin/create/', views.challenge_create, name='create'),
    path('admin/<slug:slug>/edit/', views.challenge_edit, name='edit'),
    path('admin/<slug:slug>/delete/', views.challenge_delete, name='delete'),
]
