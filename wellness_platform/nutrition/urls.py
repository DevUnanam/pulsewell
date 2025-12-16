from django.urls import path
from . import views

app_name = 'nutrition'

urlpatterns = [
    path('', views.daily_summary, name='daily_summary'),
    path('log/', views.meal_log, name='meal_log'),
    path('meal/<int:pk>/edit/', views.meal_edit, name='meal_edit'),
    path('meal/<int:pk>/delete/', views.meal_delete, name='meal_delete'),
    path('weekly/', views.weekly_summary, name='weekly_summary'),
    path('history/', views.meal_history, name='meal_history'),
    path('goals/', views.nutrition_goals, name='nutrition_goals'),
]
