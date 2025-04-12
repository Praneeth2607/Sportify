from django.urls import path
from . import views



urlpatterns = [
    path('',views.Home, name='home'),
    path('register/',views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('forgot_password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent' ),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),
    path('match/', views.profile_match_view, name='profile_match_view'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('api/ask/', views.ask_ai_api, name='ask_ai_api'),
    path('match/', views.match_form, name='match_form'),
    path('', views.index, name='index'),
    path('profile/', views.athlete_profile_view, name='profile'),
]
