from django.contrib import admin
from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', csrf_exempt(RegistrationView.as_view()) , name="register"),
    path('login', LoginView.as_view() , name="login"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()) , name="validateusername"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name="validateemail"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(),  name="activate")
]
