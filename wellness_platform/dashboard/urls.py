from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_redirect_view, name='dashboard'),
    path('user/', views.user_dashboard_view, name='user_dashboard'),
    path('admin/', views.admin_dashboard_view, name='admin_dashboard'),
]
