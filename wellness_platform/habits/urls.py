from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('create/', views.habit_create, name='habit_create'),
    path('<int:pk>/', views.habit_detail, name='habit_detail'),
    path('<int:pk>/edit/', views.habit_edit, name='habit_edit'),
    path('<int:pk>/delete/', views.habit_delete, name='habit_delete'),
    path('<int:pk>/complete/', views.habit_complete, name='habit_complete'),
    path('<int:pk>/uncomplete/', views.habit_uncomplete, name='habit_uncomplete'),
    path('<int:pk>/toggle-active/', views.habit_toggle_active, name='habit_toggle_active'),
]
