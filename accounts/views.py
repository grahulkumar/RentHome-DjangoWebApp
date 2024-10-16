from django.shortcuts import render, redirect
from accounts.models import CustomUser
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout


# login page view
def user_login(request):
    msg = ""
    success=""
    s_msg = request.GET.get("register", "")
    if s_msg:
        success="Congratulation, your account is created successfully. Now you can Sign In"

    if request.method == "POST":
        # Fetch data from form
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate user
        user_auth = authenticate(request, email=email, password=password)
        if user_auth is None:
            msg = "User does not exist, enter correct email or password"
        else:
            # Log in user
            login(request, user_auth)

            # Redirect based on user role
            if hasattr(user_auth, "role"):  # Ensure role attribute exists
                if user_auth.role == "Renter":
                    return redirect("home")
                else:
                    return redirect("owner-home")
            else:
                # Redirect to sign-in if role is not defined
                return redirect("login")
    return render(request, "accounts/login.html", {"success": success, "msg": msg})


# choose usertype page view
def user_type(request):
    return render(request, "accounts/choose_usertype.html")


# register page view
def user_register(request):
    type = request.GET.get("type")  # get user type

    # fetch data from form
    name = request.POST.get("name")
    email = request.POST.get("email")
    password = request.POST.get("password")

    # fetch data from User model to check if user already exist or not
    check_email = CustomUser.objects.filter(email=email)

    msg = ""
    if not type:
        # redirect to choose user type page
        return redirect("user-type")
    elif check_email.exists():
        msg = "Email already exist, try different email id"
    else:
        if request.method == "POST":
            user = CustomUser.objects.create(
                name=name, email=email, role=type
            )
            user.set_password(password) #convert in hash password
            user.save()

            # redirect to sign in page and add message
            url = reverse("login") + f"?register=success"
            return redirect(url)

    return render(request, "accounts/register.html", {"type": type, "msg": msg})

def user_logout(request):
    logout(request)
    return redirect('welcome')