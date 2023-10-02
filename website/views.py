from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.db import models


# Create your views here.
def home(request):
    # Check to see if logging in
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging you in")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


def login_user(request):
    pass


# Logout of current session
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')


# Sign up users
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


# View a case record by id
def case_record(request, pk):
    if request.user.is_authenticated:
        case_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'case_record': case_record})
    else:
        messages.success(request, "You must be logged in to view that page!")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('home')


def add_record(request):
    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            # Calculate the next client_num and matter_num
            if form.cleaned_data.get('matter_only'):
                # If Matter Only is selected, you can allow the user to enter their own client_num
                client_num = form.cleaned_data['client_num']
            else:
                # Otherwise, calculate the next client_num
                client_num = Record.objects.aggregate(models.Max('client_num'))['client_num__max'] or 0
                client_num += 1

            # Calculate the next matter_num
            matter_num = Record.objects.aggregate(models.Max('matter_num'))['matter_num__max'] or 0
            matter_num += 1

            # Create and save the record with the calculated values
            record = form.save(commit=False)
            record.client_num = client_num
            record.matter_num = matter_num
            record.user = request.user  # Assuming you're using user authentication
            record.save()

            # Set the initial values for client_num and matter_num in the form
            form.initial['client_num'] = client_num
            form.initial['matter_num'] = matter_num
            messages.success(request, "Record added...")
            return redirect('home')  # Redirect to the homepage or any other page as needed
    else:
        form = AddRecordForm()

    return render(request, 'add_record.html', {'form': form})


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)


