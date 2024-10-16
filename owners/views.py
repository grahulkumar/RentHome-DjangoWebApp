from django.shortcuts import render

# owner home page view
def owner_home(request):
    return render(request, "owners/owner_home.html")
