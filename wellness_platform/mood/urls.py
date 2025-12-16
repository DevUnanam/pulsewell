from django.urls import path
from . import views

app_name = 'mood'

urlpatterns = [
    path('log/', views.mood_log, name='mood_log'),
    path('history/', views.mood_history, name='mood_history'),
    path('<int:pk>/', views.mood_detail, name='mood_detail'),
    path('<int:pk>/delete/', views.mood_delete, name='mood_delete'),
]
