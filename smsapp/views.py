"""Views for StudentMS: signup and CRUD operations for StudentModel."""

import random
import string
import smtplib
from textwrap import dedent

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import StudentModel


def signup(request):
    """Handle user signup: create a user and email an initial password."""
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(username=email).exists():
            messages.error(request, "This email is already registered!")
            return render(request, "registration/signup.html")

        # Generate a simple 6-digit password (in production use a stronger flow)
        password = "".join(random.choices(string.digits, k=6))

        try:
            # Create user without keeping unused variable
            User.objects.create_user(username=email, email=email, password=password)

            subject = "Welcome to Student Management System"
            message = dedent(
                f"""\
                Your account has been created successfully!

                Email: {email}
                Password: {password}

                Please login and change your password after first login.
                """
            )

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(
                request, f"Account created! Check your email {email} for the password."
            )
            return redirect("login")

        except smtplib.SMTPException:
            # If email delivery fails, still create account — inform user on screen.
            User.objects.create_user(username=email, email=email, password=password)
            messages.success(
                request,
                f"Account created! Your password: {password} (Email delivery failed)",
            )
            return redirect("login")

    return render(request, "registration/signup.html")


@login_required
def home(request):
    """Render dashboard listing all student records and basic statistics."""
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
        "data": data,
        "total_students": total_students,
        "average_marks": average_marks,
        "highest_marks": highest_marks,
        "pass_rate": pass_rate,
    }
    return render(request, "home.html", context)


@login_required
def create(request):
    """Create a new student record using StudentForm."""
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
def delete(request, student_id):
    """Delete a student identified by student_id (primary key)."""
    student = get_object_or_404(StudentModel, student_id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect("home")


@login_required
def update(request, student_id):
    """Update an existing student record."""
    student = get_object_or_404(StudentModel, student_id=student_id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect("home")
        messages.error(request, "Please check the form data!")
    else:
        form = StudentForm(instance=student)
        form.fields["student_id"].disabled = True

    return render(request, "update.html", {"fm": form})
