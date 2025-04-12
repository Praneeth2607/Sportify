from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from django.http import JsonResponse
from .bard_helper import ask_bard_about_user
import json
import os
import pandas as pd

@login_required
def Home(request):
    return render(request, 'index.html')

def RegisterView(request):

    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False  #flag

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request,'username already exists')

        if User.objects.filter(email = email).exists():
            user_data_has_error = True
            messages.error(request, 'email already exists')
        
        if len(password)<8:
            user_data_has_error = True
            messages.error(request, 'password cannot be less than 8 characters')

        if user_data_has_error:
            return redirect('register')
        else:
            new_user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password
            )
            messages.success(request, 'Account created Successfully. Login again to get started!')
            return redirect('login')


    return render(request, 'register.html')

def LoginView(request):

    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password )
        
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else: 
            messages.error(request, "Invalid Login Credentials!")
            return redirect('login')
        
    return render(request, 'login.html')

def LogoutView(request):
    logout(request)
    return redirect('login')

def ForgotPassword(request):

    if request.method=="POST":
        email=request.POST.get('email')

        try:
            user=User.objects.get(email=email)
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link given below and DONT FORGET IT!!! :\n\n\n{full_password_reset_url}'
            
            email_message = EmailMessage(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )

            email_message.fail_silently = True
            email_message.send() 

            return redirect(reverse('password-reset-sent', kwargs={'reset_id': new_password_reset.reset_id}))

        except User.DoesNotExist:
            messages.error(request, f"No User with email {email} found ")
            return redirect('forgot-password')

    return render (request, 'forgot_password.html')

def PasswordResetSent(request, reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    
    else:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            password_has_error = False

            if password != confirm_password:
                password_has_error = True
                messages.error(request, 'Passwords do not match! Please enter the same password in both fields.')

            
            if len(password) < 8:
                password_has_error = True
                messages.error(request, 'Password must be greater than 8 characters!')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=9)

            if timezone.now() > expiration_time:
                password_has_error = True
                messages.error(request, 'Reset Link has Expired!')
                password_reset_id.delete()
                return redirect('forgot-password')

            if not password_has_error:
                user= password_reset_id.user
                user.set_password(password)
                user.save()
                password_reset_id.delete()
                messages.success(request, 'Password reset Successfully!')
                return redirect ('login')

    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
    
    return render(request, 'reset_password.html')

from core.ml_model import filter 

def profile_match_view(request):
    if request.method == 'POST':
        try:
            # Collect all filter values from the form
            filters = {
                'sport': request.POST.get('sport'),
                'age': request.POST.get('age'),
                'level': request.POST.get('level'),
            }

            matches = filter.get_top_matches(filters)
            return render(request, 'results.html', {'results': matches})

        except Exception as e:
            print(f"❌ Error in profile_match_view: {e}")
            return render(request, 'results.html', {'results': []})

    return render(request, 'match_form.html')

def match_form(request):
    if request.method == "POST":
        # Read CSV and filter based on form input
        sport = request.POST.get('sport')
        age = request.POST.get('age')
        level = request.POST.get('level')

        df = pd.read_csv('ml_model/athletes.csv')

        if sport:
            df = df[df['Sport'].str.lower() == sport.lower()]
        if age:
            df = df[df['Age'] <= int(age)]
        if level:
            df = df[df['Level'].str.lower() == level.lower()]

        matches = df.to_dict(orient='records')

        return render(request, 'results.html', {
            'matches': matches
        })

    return render(request, 'match_form.html')

def ask_ai_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        question = data.get('question')

        if not username or not question:
            return JsonResponse({'error': 'Invalid data'}, status=400)

        response = ask_bard_about_user(username, question)
        return JsonResponse({'answer': response})

def chatbot_view(request):
    return render(request, 'chatbot.html')

def index(request):
    return render(request, 'index.html')

def athlete_profile_view(request):
    return render(request, 'profile.html')

