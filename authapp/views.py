from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def Home(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        phone = request.POST.get('usernumber')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if not phone:
            messages.error(request, "Phone cannot be empty.")
            return redirect('/signup')

        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, "Phone Number must be exactly 10 digits and numeric.")
            return redirect('/signup')

        if not email:
            messages.error(request, "Email cannot be empty.")
            return redirect('/signup')

        if not password:
            messages.error(request, "Password cannot be empty.")
            return redirect('/signup')

        if password != confirmpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists.")
            return redirect('/signup')

        if User.objects.filter(username=phone).exists():
            messages.warning(request, "Phone number already exists.")
            return redirect('/signup')

        try:
            user = User.objects.create_user(
                username=phone,  
                email=email,
                password=password  
            )
            user.save()

            messages.success(request, "User created successfully. Please log in.")
            return redirect('/login')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('/signup')

    return render(request, "signup.html")

# Login View
def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get('usernumber')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/login')
    
    return render(request, "login.html")


@login_required 
def handellogout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('/login')
