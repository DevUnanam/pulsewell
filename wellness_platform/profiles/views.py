from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from django.urls import reverse
from .models import UserProfile
from .forms import UserUpdateForm, ProfileUpdateForm, AccountDeleteForm


@login_required
def profile_view(request):
    """View user profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'user': request.user,
        'profile': profile,
        'age': profile.get_age(),
        'bmi': profile.get_bmi(),
        'bmi_category': profile.get_bmi_category(),
    }
    return render(request, 'profiles/profile_view.html', context)


@login_required
def profile_edit(request):
    """Edit user profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profiles:profile_view')
        else:
            # Debug: print form errors
            if not user_form.is_valid():
                print("User form errors:", user_form.errors)
            if not profile_form.is_valid():
                print("Profile form errors:", profile_form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profiles/profile_edit.html', context)


@login_required
def account_settings(request):
    """Account settings and security"""
    return render(request, 'profiles/account_settings.html')


@login_required
def account_delete(request):
    """Delete user account"""
    if request.method == 'POST':
        form = AccountDeleteForm(request.POST)
        if form.is_valid():
            # Verify password
            user = authenticate(username=request.user.username, password=form.cleaned_data['password'])
            if user is not None:
                # Delete the user account
                username = request.user.username
                user.delete()
                logout(request)
                messages.success(request, f'Account {username} has been deleted successfully.')
                return redirect('account:login')
            else:
                messages.error(request, 'Incorrect password. Account deletion cancelled.')
        else:
            messages.error(request, 'Please confirm and enter your password.')
    else:
        form = AccountDeleteForm()

    return render(request, 'profiles/account_delete.html', {'form': form})
