from django.shortcuts import render


# Create your views here.
def under_development(request):
    return render(request, "under_development.html")
