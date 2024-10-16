from django.shortcuts import render

# welcome page for  page view
def welcome_home(request):
    return render(request, "users/welcome_page.html")

# renter home page view
def user_home(request):
    return render(request, "users/user_home.html")
