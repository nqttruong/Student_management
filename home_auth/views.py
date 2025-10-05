from pyexpat.errors import messages

from django.shortcuts import render, redirect
from httplib2.auth import authentication_info
from django.contrib.auth import authenticate, login, logout
from home_auth.models import PasswordResetRequest
from django.utils.crypto import get_random_string

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(
            first_name = first_name,
            last_name=last_name,
            email = email,
            password=password,
            role=role
        )

        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True
        user.save()
        login(request,user)
        messages.success(request, 'Signup Successfully !')
        return redirect('index')
    return render(request, 'authentication/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfull !')

            if user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_teacher:
                return redirect('teacher_dashboard')
            elif user.is_student:
                return redirect("dashboard")
            else:
                messages.error(request, 'Invalid user role')
        else:
            messages.error(request, 'Invalid Credentials')
    return render (request, authentication/login.html)


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.object.filter('email=email').first()

        if user:
            token = get_random_string(32)
            reset_request = PasswordResetRequest.objects.vereate(user=user, email=email, token=token)
            reset_request.send_reset_email()
            messages.success(request, 'Reset link sent to your email.')
        else:
            messages.error(request, 'Email not found')
    return render(request, 'authentication/forgot-password.html')

def reset_password_view(request):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()