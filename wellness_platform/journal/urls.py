from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.journal_list, name='journal_list'),
    path('new/', views.journal_create, name='journal_create'),
    path('<int:pk>/', views.journal_detail, name='journal_detail'),
    path('<int:pk>/edit/', views.journal_edit, name='journal_edit'),
    path('<int:pk>/delete/', views.journal_delete, name='journal_delete'),
]
