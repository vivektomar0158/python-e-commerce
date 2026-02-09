from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from shop.models import Category


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('shop:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('accounts:register')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return redirect('accounts:register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('accounts:register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('accounts:register')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password1
        )
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number
        )
        
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('accounts:login')
    
    context = {
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('shop:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if not remember_me:
                request.session.set_expiry(0)
            
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            
            next_url = request.GET.get('next', 'shop:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('accounts:login')
    
    context = {
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('shop:home')


@login_required
def profile_view(request):
    """User profile view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update user info
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Update profile
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.postal_code = request.POST.get('postal_code', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    context = {
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'accounts/profile.html', context)
