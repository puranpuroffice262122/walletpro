from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, OpenAccountForm, ProfileForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('wallet:dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account registered! Please open your wallet account.')
            return redirect('wallet:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('wallet:dashboard')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('wallet:dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def open_account(request):
    user = request.user
    if user.account_opened:
        return redirect('wallet:dashboard')
    if request.method == 'POST':
        form = OpenAccountForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            u = form.save(commit=False)
            u.account_opened = True
            u.account_status = 'pending'
            u.save()
            messages.success(request, 'Account application submitted! Admin will review it shortly.')
            return redirect('wallet:dashboard')
    else:
        form = OpenAccountForm(instance=user)
    return render(request, 'accounts/open_account.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
