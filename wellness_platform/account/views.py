from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def _get_redirect_url_for_user(user):
    """
    Determine the appropriate dashboard URL based on user role
    """
    if user.is_superuser or user.is_admin:
        return 'dashboard:admin_dashboard'
    return 'dashboard:user_dashboard'


def register_view(request):
    """
    Handle user registration
    """
    if request.user.is_authenticated:
        return redirect(_get_redirect_url_for_user(request.user))

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
            return redirect(_get_redirect_url_for_user(user))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handle user login - redirects to appropriate dashboard based on role
    """
    if request.user.is_authenticated:
        return redirect(_get_redirect_url_for_user(request.user))

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # Check if there's a next parameter, otherwise use role-based redirect
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                
                return redirect(_get_redirect_url_for_user(user))
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Handle user logout
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('account:login')


@login_required
def profile_view(request):
    """
    Display user profile
    """
    return render(request, 'accounts/profile.html', {'user': request.user})
