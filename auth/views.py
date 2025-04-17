from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
import uuid

from django.contrib.auth import logout
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

user_verification_tokens = {}

def user_register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=email, email=email, password=password, is_active=False)
        token = str(uuid.uuid4())
        user_verification_tokens[token] = user
        send_mail('Verify your email', f'Click to verify: http://localhost:8000/auth/verify/{token}/', 'admin@eoy.ai', [email])
        return HttpResponse("Check your email to verify your account.")
    return render(request, 'register.html')

def verify_email(request, token):
    user = user_verification_tokens.pop(token, None)
    if user:
        user.is_active = True
        user.save()
        return HttpResponse("Verified! You can login now.")
    return HttpResponse("Invalid or expired token.")

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/dashboard/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required  # Ensures that only authenticated users can access this view
def profile_view(request):
    return render(request, 'profile.html')  # Assuming you will create a 'profile.html' template


def user_logout(request):
    logout(request)
    return render(request, 'logout.html')  # Renders the logout confirmation page
