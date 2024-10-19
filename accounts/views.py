from django.shortcuts import render, redirect
from accounts.models import CustomUser, ResetPassword
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from email_services.views import send_html_email
import random
from datetime import datetime

# get current date and time from system
dateandtime = datetime.now().strftime("%I:%M %p, %d-%m-%Y")


# login page view
def user_login(request):
    msg = ""
    success = ""
    check_registered = request.GET.get("register", "")
    check_reset_password = request.GET.get("resetpassword", "")

    if check_registered:
        success = (
            "Congratulation, your account is created successfully. Now you can Login"
        )
    elif check_reset_password:
        success = (
            "Congratulation, your password is reset successfully. Now you can Login"
        )

    if request.method == "POST":
        # Fetch data from form
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate user
        user_auth = authenticate(request, email=email, password=password)
        if user_auth is None:
            msg = "Enter correct email or password"
        else:
            # Log in user
            login(request, user_auth)

            # sending mail
            email_msg = "Welcome Back to RentHome!"
            email_msg1 = f"You have successfully logged in on {dateandtime}. If this wasn't you, please click on below button to reset your password."
            email_msg2 = "Thank you for being with us!"
            forgot_password_url = "http://127.0.0.1:8000/auth/forgot-password/"
            context = {
                "name": user_auth.name,
                "message": email_msg,
                "message1": email_msg1,
                "message2": email_msg2,
                "url": forgot_password_url,
            }
            send_html_email(
                subject="Login successfully | Rent Home",
                recipient_email=user_auth.email,
                context=context,
            )

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


# Forgot password view
def user_forgot_password(request):
    msg = ""
    if request.method == "POST":
        # Fetch data from form
        email = request.POST.get("email")

        # Authenticate user
        user_email = ""
        try:
            user_detail = CustomUser.objects.get(email=email)
            user_email = user_detail.email
        except:
            pass

        if not user_email:
            msg = "User does not exist, enter correct Email ID"
        else:
            # delete previous generated code
            try:
                code_generated = ResetPassword.objects.get(user_id=user_detail.id)
                code_generated.delete()
            except:
                pass

            # generate verification code using random
            verification_code = random.randint(100000, 999999)

            # save verification code in database
            save_verification = ResetPassword.objects.create(
                user_id=user_detail.id,
                code_hash=verification_code,
                created_at=dateandtime,
            )
            save_verification.save()

            # sending mail
            email_msg = f"Your Reset code is {verification_code}. Timestamp: {dateandtime}. Use below button to reset your password."
            email_msg1 = "Do not share this code with anyone."
            email_msg2 = "Thank you for being a part of our Rent Home!"
            reset_password_url = "http://127.0.0.1:8000/auth/reset-password/"
            context = {
                "name": user_detail.name,
                "message": email_msg,
                "message1": email_msg1,
                "message2": email_msg2,
                "url": reset_password_url,
            }
            send_html_email(
                subject="Reset Password | Rent Home",
                recipient_email=user_detail.email,
                context=context,
            )

            return redirect("reset-password")
    return render(request, "accounts/forgot_password.html", {"msg": msg})


# Reset password view
def user_reset_password(request):
    msg = ""
    if request.method == "POST":
        # Fetch data from form
        verify_code = request.POST.get("verifycode")
        new_password = request.POST.get("password")

        # verify user entered code
        user_id = ""
        try:
            check_entered_code = ResetPassword.objects.get(code_hash=verify_code)
            user_id = check_entered_code.user_id
        except:
            pass

        if not user_id:
            msg = "Incorrect Verification code"
        else:
            # delete code from database
            check_entered_code.delete()

            # reset password
            reset_password = CustomUser.objects.get(id=user_id)
            reset_password.set_password(new_password)
            reset_password.save()

            # get user details
            user_detail = CustomUser.objects.get(id=user_id)

            # send confirmation mail
            email_msg = "Password Reset Successful!"
            email_msg1 = f"Your password has been reset successfully. Timestamp: {dateandtime}. Use below button to login."
            email_msg2 = "Thank you for being a part of our Rent Home!"
            login_url = "http://127.0.0.1:8000/auth/login/"
            context = {
                "name": user_detail.name,
                "message": email_msg,
                "message1": email_msg1,
                "message2": email_msg2,
                "url": login_url,
            }
            send_html_email(
                subject="Reset password successfully | Rent Home",
                recipient_email=user_detail.email,
                context=context,
            )

            # redirect to login page and add message
            url = reverse("login") + f"?resetpassword=success"
            return redirect(url)
    return render(request, "accounts/reset_user_password.html", {"msg": msg})


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
            user = CustomUser.objects.create(name=name, email=email, role=type)
            user.set_password(password)  # convert in hash password
            user.save()

            # sending mail
            email_msg = "Congratulations!"
            email_msg1 = f" You have successfully created your account on Rent Home on {dateandtime}. We’re excited to have you on board! Explore our platform to find your perfect home."
            email_msg2 = "Happy renting!"
            login_url = "http://127.0.0.1:8000/auth/login/"
            context = {
                "name": name,
                "message": email_msg,
                "message1": email_msg1,
                "message2": email_msg2,
                "url": login_url,
            }
            send_html_email(
                subject="Account created successfully | Rent Home",
                recipient_email=email,
                context=context,
            )

            # redirect to sign in page and add message
            url = reverse("login") + f"?register=success"
            return redirect(url)

    return render(request, "accounts/register.html", {"type": type, "msg": msg})


def user_logout(request):
    #get user details
    user_details=request.user
    #sending mail
    email_msg = f"You have successfully logged out on {dateandtime}."
    email_msg1 = "See you soon!"
    context = {
        "name": user_details.name,
        "message": email_msg,
        "message1": email_msg1,
    }
    send_html_email(
        subject="Logout successfully | Rent Home",
        recipient_email=user_details.email,
        context=context,
    )

    logout(request)
    return redirect("welcome")
