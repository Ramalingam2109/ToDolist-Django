from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    if request.method == "POST":
        task = request.POST.get('task')
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()
        return redirect('home-page')  # Redirect to avoid duplicate submissions
        
    all_to_dos = todo.objects.filter(user=request.user)  # Changed User to user
    context = {
        'todos': all_to_dos
    }
    return render(request, "todoapp/todo.html", context)  # Added context

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('register')
        
        get_all_users_by_username = User.objects.filter(username=username)
        
        if get_all_users_by_username:
            messages.error(request, "Error: username already exists")
            return redirect('register')
        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.success(request, "User successfully created, login now")
        return redirect("login")
    return render(request, "todoapp/register.html", {})

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        
        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect("home-page")
        else:
            messages.error(request, "Error: wrong user details or user doesn't exist")
            return redirect('login')
    return render(request, "todoapp/login.html", {})  # Fixed syntax error

@login_required
def LogoutView(request):
    logout(request)
    return redirect('login')  # Fixed redirect (added quotes)

@login_required
def DeleteTask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)  # Changed User to user
    get_todo.delete()
    return redirect("home-page")

@login_required
def UpdateTask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect("home-page")  # Added redirect