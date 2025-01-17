from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.hashers import check_password as verify_pass
from .models import get_user_by_email, check_password, create_user, serialize


def Login(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get('login_email')
        password = request.POST.get('login_password')
        
        # Check if user exists
        user = get_user_by_email(email)
        if not user:
            return "User not found"
        
        # Verify password
        if not verify_pass(password, user["password"]):
            return "Password incorrect!"
        
        # Set session
        request.session["user_id"] = str(user["_id"])
        request.session["user"] = serialize(user)
        request.session["logged_in"] = True
        return ""

    return "Invalid request method"


def LoginPage(request: HttpRequest):
    if request.session.get("logged_in"):
        return redirect("home")

    error = ""
    if request.method == "POST":
        error = Login(request)
        if not error:
            return redirect("home")

    return render(request, "Login.html", {"error": error})

def Register(request: HttpRequest):
    # Validate email
    email = request.POST.get("register_email")
    if not email:
        return "Email is required!"
    
    if get_user_by_email(email):
        return "Email already taken!"
    
    # Validate password
    password = request.POST.get("register_password")
    if not password:
        return "Password is required!"
    
    valid, msg = check_password(password)
    if not valid:
        return msg

    # Validate password confirmation
    password_confirm = request.POST.get("register_password_confirm")
    if not password_confirm:
        return "Password confirmation is required!"
    
    if password != password_confirm:
        return "Passwords do not match!"

    # Create user
    user = create_user(email, password)
    if user:
        return ""
    else:
        return "There was an error creating the user!"


def RegisterPage(request:HttpRequest):
    
    if (request.session.get("logged_in")):
       return redirect("home")
    error = ""
    if (request.method == "POST"):
        error = Register(request)
        if (not error or error == ""):
            return redirect("Login")
    return render(request, "Register.html", {
        "error": error
    })


def LogoutPage(request: HttpRequest):
    request.session.clear()
    return redirect("home")
