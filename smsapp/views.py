from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from .forms import StudentForm
from .models import StudentModel

# ===== SIGNUP FUNCTION =====
def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "This email is already registered!")
            return render(request, "registration/signup.html")
        
        # Generate random 6-digit password
        password = ''.join(random.choices(string.digits, k=6))
        
        try:
            # Create user
            user = User.objects.create_user(username=email, email=email, password=password)
            
            # Send email with password
            subject = "Welcome to Student Management System"
            message = f"""
Your account has been created successfully!

Email: {email}
Password: {password}	

Please login and change your password after first login.
"""
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, f"Account created! Check your email {email} for the password.")
            return redirect("login")
            
        except Exception as e:
            # If email fails, still create user but show password on screen
            user = User.objects.create_user(username=email, email=email, password=password)
            messages.success(request, f"Account created! Your password: {password} (Email delivery failed)")
            return redirect("login")
    
    return render(request, "registration/signup.html")

# ===== YOUR EXISTING CRUD VIEWS =====
@login_required
def home(request):
    data = StudentModel.objects.all()
    total_students = data.count()
    
    if total_students > 0:
        total_marks = sum(float(student.marks) for student in data)
        average_marks = round(total_marks / total_students, 2)
        highest_marks = max(float(student.marks) for student in data)
        passed_students = sum(1 for student in data if float(student.marks) >= 40)
        pass_rate = round((passed_students / total_students) * 100, 2)
    else:
        average_marks = highest_marks = pass_rate = 0
    
    context = {
        'data': data,
        'total_students': total_students,
        'average_marks': average_marks,
        'highest_marks': highest_marks,
        'pass_rate': pass_rate,
    }
    return render(request, "home.html", context)

@login_required
def create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Student added successfully!")
                return redirect("home")
            except IntegrityError:
                messages.error(request, "Student ID already exists!")
        else:
            messages.error(request, "Please check the form data!")
    else:
        form = StudentForm()
    
    return render(request, "create.html", {"fm": form})

@login_required
def delete(request, id):
    student = get_object_or_404(StudentModel, student_id=id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect("home")

@login_required
def update(request, id):
    student = get_object_or_404(StudentModel, student_id=id)
    
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect("home")
        else:
            messages.error(request, "Please check the form data!")
    else:
        form = StudentForm(instance=student)
        form.fields['student_id'].disabled = True
    
    return render(request, "update.html", {"fm": form})