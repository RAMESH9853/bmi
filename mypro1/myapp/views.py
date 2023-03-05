from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string

from .forms import RegistrationForm, LoginForm
from .models import User


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            token = get_random_string(length=32)
            user.token = token
            user.save()
            link = reverse('verify_email', args=[token])
            url = request.build_absolute_uri(link)
            subject = 'Verify Your Email'
            message = f'Hi {user.username},\n\nPlease click on the following link to verify your email:\n{url}\n\nThanks!'
            from_email = 'noreply@myapp.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return render(request, 'registration/registration_success.html', {'email': user.email})
    else:
        form = RegistrationForm()
        return render(request, 'registration/registration.html', {'form': form})


def verify_email(request, token):
    user = User.objects.get(token=token)
    user.is_active = True
    user.token = ''
    user.save()
    return render(request, 'registration/verify_email.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'registration/login.html', {'form': form, 'error_message': 'Your account is inactive.'})
            else:
                return render(request, 'registration/login.html', {'form': form, 'error_message': 'Invalid email or password.'})
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer


@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        serializer = ProfileSerializer(profile, data=request.POST)
        if serializer.is_valid():
            serializer.save()
    else:
        serializer = ProfileSerializer(profile)
    return render(request, 'profile.html', {'profile': serializer.data})
