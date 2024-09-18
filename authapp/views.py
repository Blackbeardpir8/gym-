from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authapp.models import Contact,Enrollment,Membership_Plan,Trainer,Attendance
from datetime import datetime
from django.db.models import Count
from django.urls import reverse


def Home(request):
    return render(request, "index.html")

def profile(request, enroll_id=None):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in and try again.")
        return redirect('/login')
    user_phone = request.user
    posts = Enrollment.objects.filter(phone=user_phone)
    context = {"posts":posts}
    return render(request, "profile.html",context)


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

    if not request.user.is_authenticated:
        messages.warning(request, "Please log in and try again.")
        return redirect('/login')

    
    memberships = Membership_Plan.objects.all().order_by('price')
    trainers = Trainer.objects.all()
    context = {"memberships": memberships, "trainers": trainers}

    if request.method == "POST":
        
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

        try:
            membership = Membership_Plan.objects.get(id=member_id)
            trainer = Trainer.objects.get(id=trainer_id)
        except Membership_Plan.DoesNotExist:
            messages.error(request, "Selected membership does not exist.")
            return redirect('enroll')
        except Trainer.DoesNotExist:
            messages.error(request, "Selected trainer does not exist.")
            return redirect('enroll')

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
            emergency_contact=emergency_contact  
        )

        query.save()

        messages.success(request, "Thanks for enrolling!")
        return redirect('/')

    return render(request, "enroll.html", context)


def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in and try again.")
        return redirect('/login')
    
    select_trainer = Trainer.objects.all()
    context = {"SelectTrainer": select_trainer}

    if request.method == 'POST':
        phone = request.POST.get('phone')
        select_date = request.POST.get('select_date')
        login_time = request.POST.get('login')
        logout_time = request.POST.get('logout')
        workout_type = request.POST.get('select_workout')
        trainer_id = request.POST.get('trained_by')

        if not (select_date and login_time and logout_time and workout_type and trainer_id):
            messages.error(request, "All fields are required.")
            return render(request, "attendance.html", context)

        try:
            trainer = Trainer.objects.get(id=trainer_id)
        except Trainer.DoesNotExist:
            messages.error(request, "Selected trainer does not exist.")
            return render(request, "attendance.html", context)

        attendance = Attendance(
            phone=phone,
            select_date=select_date,
            login=login_time,
            logout=logout_time,
            select_workout=workout_type,
            trained_by=trainer
        )
        attendance.save() 
        messages.success(request, "Attendance recorded successfully!")
        return redirect('attendance') 

    return render(request, "attendance.html", context)

    return render(request, "attendance.html", context)


def tracker(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in and try again.")
        return redirect('/login')
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    months = [
        ('01', 'January'), ('02', 'February'), ('03', 'March'),
        ('04', 'April'), ('05', 'May'), ('06', 'June'),
        ('07', 'July'), ('08', 'August'), ('09', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December')
    ]
    years = [str(year) for year in range(current_year - 10, current_year + 1)]

    selected_year = request.GET.get('year', str(current_year))
    selected_month = request.GET.get('month', str(current_month).zfill(2))

    valid_years = years
    valid_months = dict(months).keys()
    if selected_year not in valid_years:
        selected_year = str(current_year)
    if selected_month not in valid_months:
        selected_month = str(current_month).zfill(2)

    attendance_records = Attendance.objects.filter(
        phone=request.user.username,
        select_date__year=selected_year,
        select_date__month=selected_month
    )

    monthly_attendance = (
        Attendance.objects.filter(phone=request.user.username)
        .values('select_date__year', 'select_date__month')
        .annotate(total_attendance=Count('id'))
        .order_by('select_date__year', 'select_date__month')
    )

    workout_types = Attendance.objects.values_list('select_workout', flat=True).distinct()

    print("Monthly Attendance:", list(monthly_attendance))
    print("Attendance Records:", list(attendance_records))
    print("Workout Types:", list(workout_types))

    context = {
        'monthly_attendance': monthly_attendance,
        'attendance': attendance_records,
        'months': months,
        'years': years,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'workout_types': workout_types
    }
    return render(request, "tracker.html", context)

def services(request):
    return render(request,"services.html")
