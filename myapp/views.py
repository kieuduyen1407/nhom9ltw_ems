from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request, 'home.html')
def profile(request):
    bien=Profile.objects.all()
    return render(request, 'profile.html', {'emps': bien})
def about(request):
    return render(request,'about.html')
def profile_detail(request, id):
    emp = get_object_or_404(Profile, id=id)
    return render(request,'profile_detail.html', {'emp': emp})
def logout(request):
    return redirect('/')
def login(request):
    return redirect('/')
