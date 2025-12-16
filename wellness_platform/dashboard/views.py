from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    """
    Display the main dashboard for authenticated users
    """
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard/dashboard.html', context)
