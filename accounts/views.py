from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm, UserLoginForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Welcome to GAB Platform, {user.get_full_name() or user.username}! "
                f"Your account as {user.get_role_display()} has been created successfully."
            )
            return redirect(user.get_dashboard_url())
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'page_title': 'Create Account - GAB Platform'
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect(user.get_dashboard_url())
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'page_title': 'Login - GAB Platform'
    })


@require_http_methods(["POST", "GET"])
def logout_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.info(request, f"You have been logged out successfully. See you soon, {username}!")
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user_obj': request.user,
        'page_title': 'My Profile - GAB Platform'
    })


@login_required
def industry_dashboard(request):
    if not request.user.is_industry:
        messages.warning(request, "Access denied. This dashboard is only for Industry users.")
        return redirect(request.user.get_dashboard_url())
    return render(request, 'accounts/dashboards/industry.html', {
        'page_title': 'Industry Dashboard - GAB'
    })


@login_required
def wholesaler_dashboard(request):
    if not request.user.is_wholesaler:
        messages.warning(request, "Access denied. This dashboard is only for Wholesaler users.")
        return redirect(request.user.get_dashboard_url())
    return render(request, 'accounts/dashboards/wholesaler.html', {
        'page_title': 'Wholesaler Dashboard - GAB'
    })


@login_required
def shopkeeper_dashboard(request):
    if not request.user.is_shopkeeper:
        messages.warning(request, "Access denied. This dashboard is only for Shopkeeper users.")
        return redirect(request.user.get_dashboard_url())
    return render(request, 'accounts/dashboards/shopkeeper.html', {
        'page_title': 'Shopkeeper Dashboard - GAB'
    })


@login_required
def buyer_dashboard(request):
    if not request.user.is_buyer:
        messages.warning(request, "Access denied. This dashboard is only for Buyer users.")
        return redirect(request.user.get_dashboard_url())
    return render(request, 'accounts/dashboards/buyer.html', {
        'page_title': 'Buyer Dashboard - GAB'
    })
