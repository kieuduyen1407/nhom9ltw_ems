from django.shortcuts import render, get_object_or_404, redirect
from .forms import SignUpForm, SignInForm, UserForm, ProfileForm
from .models import Profile, Sheet, Position, Department
from django.contrib.auth.models import User, auth
from datetime import datetime
from django.db.models import Sum
from django.contrib import messages

# Create your views here.
def home(request):
    title = 'Home'
    context = {'title': title}
    return render(request, 'pages/home.html', context)

def register(request):
    title = 'Đăng ký'
    form_rg = SignUpForm()
    if request.POST:
        form_rg = SignUpForm(request.POST)
        if form_rg.is_valid():
            user = form_rg.save()
            profile = Profile.objects.create(user = user, 
                                             gender = form_rg.cleaned_data['gender'],
                                             dob=form_rg.cleaned_data['dob'], 
                                             phone_number=form_rg.cleaned_data['phone_number'], 
                                             address=form_rg.cleaned_data['address'])
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
        if user is not None and user.profile.end_date is None:  # Nếu có user thì login
            auth.login(request, user)
            return redirect('/')
        elif user.profile.end_date is not None:
            messages.error(request, 'Bạn không còn là nhân viên')
            return redirect('/')
        else:
            messages.error(request, 'Tài khoản hoặc mật khẩu không đúng')
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
            positions = Position.objects.all()
            departments = Department.objects.all()
            if request.POST:
                pos = request.POST.get('position')
                dep = request.POST.get('department')
                position = Position.objects.get(name=pos)
                department = Department.objects.get(name=dep)
                user.profile.position = position
                user.profile.department = department
                user.profile.save()
            context = {'title':title,
                       'user':user,
                       'positions': positions,
                       'departments': departments}
            return render(request, 'pages/profile_detail.html', context)
        else:
            messages.warning(request, 'Vào của mày mà xem')
            return redirect('profile_detail', username=request.user.username)
    else:
        messages.error(request, 'Không tìm thấy người dùng này')
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
        messages.warning(request, 'Mày đừng có mà táy máy')
        return redirect('profile_detail', username = request.user.username)

def time_keeping(request):
    if request.user.is_authenticated:
        title = 'Check In'
        date = datetime.now().date()
        if request.POST:
            check = request.POST.get('check', '')
            if check == 'in':
                Sheet.objects.create(user=request.user,date=datetime.now().date(),checkin=datetime.now().time())
            if check == 'out':
                sheet = Sheet.objects.get(user=request.user, date=datetime.now().date())
                sheet.checkout = datetime.now().time()
                sheet.save()
            return redirect('home')
        context = {'title': title, 'date': date}
        return render(request, 'pages/time_keeping.html', context)
    else:
        messages.error(request, 'Vui lòng đăng nhập')
        return redirect('home')
    
def sheet(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    if user and request.user.is_authenticated:
        if request.user.username == username:
            title = f'Bảng chấm công {username}'
            sheets = Sheet.objects.filter(user=user).order_by('-date')
            sheets.total_hour = sheets.aggregate(total_hour=Sum('work_hour'))['total_hour']
            sheets.total_salary = sheets.aggregate(total_salary=Sum('salary'))['total_salary']
            sheets.count_late = sheets.filter(status='Muộn').count()
            context = {'title': title,
                       'sheets': sheets}
            return render(request, 'pages/sheet.html', context)
        else:
            messages.warning(request, 'Vào của mày mà xem')
            return redirect('sheet', username=request.user.username)
    else:
        messages.error(request, 'Vui lòng đăng nhập')
        return redirect('home')