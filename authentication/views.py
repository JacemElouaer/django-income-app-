from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.mail import EmailMessage
from .utils import token_generator


# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # get the data
        # Validate
        # create a user account
        context = {
            'validField': request.POST
        }
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'password too short');
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)

                uidb64 = urlsafe_base64_encode(force_bytes(user.id))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = 'http://' + domain + link

                email_subject = "Activate your app"
                email_body = "hi" + user.username + " please use this link to verify your account \n" + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,

                    'jassemelwaar@gmail.com',
                    [email],
                )
                email.send(fail_silently=False)
                user.save()
                messages.success(request, 'user created successful');
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')

        # messages.success(request , "Registration was successfully :) ")
        # return  render(request,'authentication/register.html')


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({"username_error": "username should only contain alphanumeric characters"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "sorry username already used"}, status=409)
        return JsonResponse({"username_valid": True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        print(email)
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"email_error": "this email is invalid  !! "}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "sorry email already used"}, status=409)
        return JsonResponse({"email_valid": True})


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_encode(uidb64))
            user = User.objects.get(id=id)

            if not token_generator.check_token(user, token):
                return redirect('login' + '?message=' + 'User already activated')
            if user.is_active:
                return redirect('login')
            user.is_active

            messages.success(request, 'Account activated successfully')
            return redirect('login')


        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
