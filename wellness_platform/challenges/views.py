from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import date, timedelta
from .models import Challenge, UserChallenge, DailyCheckIn, ChallengeBadge


def is_superuser(user):
    """Check if user is a superuser"""
    return user.is_superuser


@login_required
def challenge_explore(request):
    """Explore/catalog page with filters and pagination"""
    challenges = Challenge.objects.filter(is_active=True)

    # Get filter parameters
    difficulty = request.GET.get('difficulty', '')
    goal_type = request.GET.get('goal_type', '')
    duration = request.GET.get('duration', '')
    search = request.GET.get('search', '')

    # Apply filters
    if difficulty:
        challenges = challenges.filter(difficulty=difficulty)

    if goal_type:
        challenges = challenges.filter(goal_type=goal_type)

    if duration:
        if duration == 'short':
            challenges = challenges.filter(duration_days__lte=7)
        elif duration == 'medium':
            challenges = challenges.filter(duration_days__gt=7, duration_days__lte=21)
        elif duration == 'long':
            challenges = challenges.filter(duration_days__gt=21)

    if search:
        challenges = challenges.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(daily_requirement__icontains=search)
        )

    # Get user's active challenges to mark as joined
    user_challenge_ids = []
    if request.user.is_authenticated:
        user_challenge_ids = UserChallenge.objects.filter(
            user=request.user,
            status='active'
        ).values_list('challenge_id', flat=True)

    # Pagination - 10 per page
    paginator = Paginator(challenges, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'user_challenge_ids': list(user_challenge_ids),
        'difficulty': difficulty,
        'goal_type': goal_type,
        'duration': duration,
        'search': search,
        'difficulty_choices': Challenge.DIFFICULTY_CHOICES,
        'goal_type_choices': Challenge.GOAL_TYPE_CHOICES,
    }
    return render(request, 'challenges/explore.html', context)


@login_required
def challenge_detail(request, slug):
    """Challenge detail page"""
    challenge = get_object_or_404(Challenge, slug=slug, is_active=True)

    # Check if user has already joined
    user_challenge = UserChallenge.objects.filter(
        user=request.user,
        challenge=challenge,
        status='active'
    ).first()

    # Get recent participants
    recent_participants = UserChallenge.objects.filter(
        challenge=challenge
    ).select_related('user').order_by('-joined_at')[:10]

    context = {
        'challenge': challenge,
        'user_challenge': user_challenge,
        'recent_participants': recent_participants,
        'is_joined': user_challenge is not None,
        'is_full': challenge.is_full(),
    }
    return render(request, 'challenges/detail.html', context)


@login_required
def challenge_join(request, slug):
    """Join a challenge"""
    challenge = get_object_or_404(Challenge, slug=slug, is_active=True)

    # Check if challenge is full
    if challenge.is_full():
        messages.error(request, 'This challenge is full!')
        return redirect('challenges:detail', slug=slug)

    # Check if user already joined
    existing = UserChallenge.objects.filter(
        user=request.user,
        challenge=challenge,
        status='active'
    ).exists()

    if existing:
        messages.warning(request, 'You have already joined this challenge!')
        return redirect('challenges:detail', slug=slug)

    # Create UserChallenge
    user_challenge = UserChallenge.objects.create(
        user=request.user,
        challenge=challenge,
        start_date=date.today()
    )

    messages.success(request, f'Successfully joined "{challenge.title}"! Good luck! 🎉')
    return redirect('challenges:my_challenge', pk=user_challenge.pk)


@login_required
def my_challenges(request):
    """User's active and completed challenges"""
    active_challenges = UserChallenge.objects.filter(
        user=request.user,
        status='active'
    ).select_related('challenge').order_by('-joined_at')

    completed_challenges = UserChallenge.objects.filter(
        user=request.user,
        status='completed'
    ).select_related('challenge').order_by('-completed_at')

    # Get total stats
    stats = UserChallenge.objects.filter(user=request.user).aggregate(
        total_points=Sum('points_earned'),
        total_completed=Count('id', filter=Q(status='completed'))
    )

    total_badges = ChallengeBadge.objects.filter(user=request.user).count()

    context = {
        'active_challenges': active_challenges,
        'completed_challenges': completed_challenges,
        'total_points': stats['total_points'] or 0,
        'total_completed': stats['total_completed'] or 0,
        'total_badges': total_badges,
    }
    return render(request, 'challenges/my_challenges.html', context)


@login_required
def my_challenge_detail(request, pk):
    """Detailed view of user's challenge with progress tracking"""
    user_challenge = get_object_or_404(
        UserChallenge,
        pk=pk,
        user=request.user
    )

    # Get check-ins
    check_ins = user_challenge.check_ins.order_by('-date')[:30]

    # Get today's check-in
    today = date.today()
    today_checkin = user_challenge.check_ins.filter(date=today).first()

    # Calculate calendar data (last 30 days)
    calendar_data = []
    for i in range(30):
        check_date = today - timedelta(days=i)
        checkin = user_challenge.check_ins.filter(date=check_date).first()
        calendar_data.append({
            'date': check_date,
            'completed': checkin.completed if checkin else False,
            'has_checkin': checkin is not None
        })

    context = {
        'user_challenge': user_challenge,
        'check_ins': check_ins,
        'today_checkin': today_checkin,
        'calendar_data': calendar_data,
        'can_checkin': not today_checkin and user_challenge.is_active(),
    }
    return render(request, 'challenges/my_challenge_detail.html', context)


@login_required
def daily_checkin(request, pk):
    """Daily check-in for a challenge"""
    user_challenge = get_object_or_404(
        UserChallenge,
        pk=pk,
        user=request.user,
        status='active'
    )

    today = date.today()

    # Check if already checked in today
    existing_checkin = DailyCheckIn.objects.filter(
        user_challenge=user_challenge,
        date=today
    ).first()

    if existing_checkin:
        messages.warning(request, 'You have already checked in today!')
        return redirect('challenges:my_challenge', pk=pk)

    if request.method == 'POST':
        # Get form data
        completed = request.POST.get('completed') == 'on'
        value_logged = request.POST.get('value_logged', '')
        mood = request.POST.get('mood', '')
        difficulty = request.POST.get('difficulty', '')
        notes = request.POST.get('notes', '')

        # Create check-in
        checkin = DailyCheckIn.objects.create(
            user_challenge=user_challenge,
            date=today,
            completed=completed,
            value_logged=float(value_logged) if value_logged else None,
            mood=mood,
            difficulty=difficulty,
            notes=notes
        )

        if completed:
            messages.success(request, '🎉 Great job! Check-in recorded successfully!')
        else:
            messages.info(request, 'Check-in recorded. Keep pushing!')

        return redirect('challenges:my_challenge', pk=pk)

    context = {
        'user_challenge': user_challenge,
        'challenge': user_challenge.challenge,
    }
    return render(request, 'challenges/daily_checkin.html', context)


@login_required
def recommended_challenges(request):
    """Smart personalized challenge recommendations"""
    # Get user profile
    try:
        profile = request.user.profile
    except:
        messages.info(request, 'Complete your profile to get personalized recommendations!')
        return redirect('challenges:explore')

    recommended = []

    # BMI-based recommendations
    bmi = profile.get_bmi()
    if bmi:
        if bmi > 25:
            # Recommend weight loss challenges
            recommended.extend(
                Challenge.objects.filter(
                    is_active=True,
                    goal_type='weight'
                )[:3]
            )
        elif bmi < 18.5:
            # Recommend nutrition challenges
            recommended.extend(
                Challenge.objects.filter(
                    is_active=True,
                    goal_type='nutrition'
                )[:3]
            )

    # Wellness goals-based recommendations
    if profile.wellness_goals:
        goals_lower = profile.wellness_goals.lower()
        if 'stress' in goals_lower or 'mental' in goals_lower or 'anxiety' in goals_lower:
            recommended.extend(
                Challenge.objects.filter(
                    is_active=True,
                    goal_type='mental_health'
                )[:3]
            )
        if 'fitness' in goals_lower or 'exercise' in goals_lower:
            recommended.extend(
                Challenge.objects.filter(
                    is_active=True,
                    goal_type='fitness'
                )[:3]
            )

    # Remove duplicates
    seen = set()
    unique_recommended = []
    for challenge in recommended:
        if challenge.id not in seen:
            seen.add(challenge.id)
            unique_recommended.append(challenge)

    # If no recommendations, show beginner challenges
    if not unique_recommended:
        unique_recommended = Challenge.objects.filter(
            is_active=True,
            difficulty='beginner'
        )[:6]

    context = {
        'recommended_challenges': unique_recommended,
        'profile': profile,
    }
    return render(request, 'challenges/recommended.html', context)


# Admin-only views
@login_required
@user_passes_test(is_superuser)
def challenge_create(request):
    """Create a new challenge (admin only)"""
    from .forms import ChallengeForm

    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.created_by = request.user
            challenge.save()
            messages.success(request, f'Challenge "{challenge.title}" created successfully!')
            return redirect('challenges:detail', slug=challenge.slug)
    else:
        form = ChallengeForm()

    context = {'form': form}
    return render(request, 'challenges/challenge_form.html', context)


@login_required
@user_passes_test(is_superuser)
def challenge_edit(request, slug):
    """Edit a challenge (admin only)"""
    from .forms import ChallengeForm

    challenge = get_object_or_404(Challenge, slug=slug)

    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES, instance=challenge)
        if form.is_valid():
            form.save()
            messages.success(request, f'Challenge "{challenge.title}" updated successfully!')
            return redirect('challenges:detail', slug=challenge.slug)
    else:
        form = ChallengeForm(instance=challenge)

    context = {'form': form, 'challenge': challenge}
    return render(request, 'challenges/challenge_form.html', context)


@login_required
@user_passes_test(is_superuser)
def challenge_delete(request, slug):
    """Delete a challenge (admin only)"""
    challenge = get_object_or_404(Challenge, slug=slug)

    if request.method == 'POST':
        title = challenge.title
        challenge.delete()
        messages.success(request, f'Challenge "{title}" deleted successfully!')
        return redirect('challenges:explore')

    context = {'challenge': challenge}
    return render(request, 'challenges/challenge_confirm_delete.html', context)
