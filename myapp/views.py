from django.shortcuts import render, get_object_or_404, redirect
from .forms import SignUpForm, SignInForm, UserForm, ProfileForm
from .models import Profile, Sheet
from django.contrib.auth.models import User, auth
from datetime import datetime


# Create your views here.
def home(request):
    title = 'Home'
    context = {'title': title}
    return render(request, 'pages/home.html', context)

def profile(request):
    bien=Profile.objects.all()
    return render(request, 'profile.html', {'emps': bien})

def about(request):
    return render(request,'pages/about.html')

def profile_detail(request, id):
    emp = get_object_or_404(Profile, id=id)
    return render(request,'profile_detail.html', {'emp': emp})

def register(request):
    title = 'Đăng ký'
    form_rg = SignUpForm()
    if request.POST:
        form_rg = SignUpForm(request.POST)
        if form_rg.is_valid():
            user = form_rg.save()
            profile = Profile.objects.create(user = user, dob=form_rg.cleaned_data['dob'], phone_number=form_rg.cleaned_data['phone_number'], address=form_rg.cleaned_data['address'])
            profile.save()
            return redirect('login')
    context = {'title': title,
               'form_rg': form_rg}
    return render(request, 'pages/register.html', context)

def login(request):
    title = 'Đăng nhập'
    form_li = SignInForm()
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:  # Nếu có user thì login
            auth.login(request, user)
            return redirect('/')
        else:
            return redirect('login')
    context = {'title': title,
               'form_li':form_li}
    return render(request, 'pages/login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')

def profile_detail(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    if user:
        if request.user.is_superuser or request.user.username == username:
            title = f'Hồ sơ {username}'
            context = {'title':title,
                       'user':user}
            return render(request, 'pages/profile_detail.html', context)
        else:
            return redirect('profile_detail', username=request.user.username)
    else:
        return redirect('home')

def update_info(request, username):
    if request.user.username==username:
        title = f'Sửa hồ sơ {username}'
        form_user = UserForm(instance=request.user)
        form_pr = ProfileForm(instance=request.user.profile)
        if request.POST:
            form_user = UserForm(request.POST, instance=request.user)
            form_pr = ProfileForm(request.POST, instance=request.user.profile)
            if form_user.is_valid() and form_pr.is_valid():
                form_user.save()
                form_pr.save()
                return redirect('profile_detail', username = request.user.username)
        context = {'title': title,
                   'form_user':form_user,
                   'form_pr':form_pr}
        return render(request, 'pages/update_info.html', context)
    else:
        return redirect('profile_detail', username = request.user.username)

def time_keeping(request):
    if request.user.is_authenticated:
        title = 'Check In'
        date = datetime.now().date()
        if request.POST:
            checkin = request.POST.get('checkin', '')
            checkout = request.POST.get('checkout', '')
            if checkin:
                Sheet.objects.create(user=request.user,date=datetime.now().date(),checkin=datetime.now().time())
            if checkout:
                sheet = Sheet.objects.get(user=request.user, date=datetime.now().date())
                sheet.checkout = datetime.now().time()
                sheet.save()
            return redirect('home')
        context = {'title': title, 'date': date}
        return render(request, 'pages/time_keeping.html', context)
    else:
        return redirect('home')