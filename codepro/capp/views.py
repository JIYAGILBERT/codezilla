from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

# Create your views here.

# signup

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationsForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationsForm()
    return render(request, 'signup.html', {'form': form})


# login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # check superuser or not
            if user.is_superuser or user.is_staff:
                return redirect('admin_home')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# admin check function
def is_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_admin)
def admin_home(request):
    return render(request, 'admin_home.html')

@login_required(login_url='login')
def home_view(request):
    return render(request, 'home.html')


