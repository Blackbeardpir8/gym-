from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authapp.models import Contact,Enrollment,Membership_Plan,Trainer


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


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        description = request.POST.get('description')

        user_contact = Contact(name=name, email=email, phone=phone, description=description)
        user_contact.save()

        messages.info(request, "Thanks for contacting us! We will get back to you as soon as possible.")

        return redirect('/contact')

    return render(request, "contact.html")


def enroll(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in and try again.")
        return redirect('/login')

    # Get memberships and trainers to display in the form
    memberships = Membership_Plan.objects.all().order_by('price')
    trainers = Trainer.objects.all()
    context = {"memberships": memberships, "trainers": trainers}

    if request.method == "POST":
        # Get form data
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone')
        dob = request.POST.get('dob')
        member_id = request.POST.get('select_membership')
        trainer_id = request.POST.get('trainer')
        reference = request.POST.get('reference')
        address = request.POST.get('address')
        emergency_contact = request.POST.get('emergency_contact')

        # Get the selected membership and trainer
        try:
            membership = Membership_Plan.objects.get(id=member_id)
            trainer = Trainer.objects.get(id=trainer_id)
        except Membership_Plan.DoesNotExist:
            messages.error(request, "Selected membership does not exist.")
            return redirect('enroll')
        except Trainer.DoesNotExist:
            messages.error(request, "Selected trainer does not exist.")
            return redirect('enroll')

        # Create a new Enrollment entry
        query = Enrollment(
            fullname=fullname,
            email=email,
            gender=gender,
            phone=phone_number,
            dob=dob,
            select_membership=membership,
            select_trainer=trainer,
            reference=reference,
            address=address,
            emergency_contact=emergency_contact  # Save emergency contact
        )

        # Save the enrollment data to the database
        query.save()

        # Display a success message and redirect
        messages.success(request, "Thanks for enrolling!")
        return redirect('/')

    return render(request, "enroll.html", context)
