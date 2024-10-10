from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib import messages
from datetime import datetime
from myapp.models import Sheet, User, Profile, Position, Department
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
  if request.user.is_superuser:
    title = 'Dashboard'
    count_emp_male = User.objects.filter(profile__gender='Nam').count()
    count_emp_female = User.objects.filter(profile__gender='Nữ').count()
    count_position = Position.objects.all().count()
    count_department = Department.objects.all().count()
    context = {'title': title,
               'count_emp_male': count_emp_male,
               'count_emp_female': count_emp_female,
               'count_position': count_position,
               'count_department': count_department}
    return render(request, 'pages/management.html', context)
  else:
    messages.warning(request, 'Không có quyền truy cập')
    return redirect('/')

def employee(request):
  if request.user.is_superuser:
    title = 'Tất cả nhân viên'
    emps = User.objects.exclude(username='admin').order_by('-profile__start_date')
    positions = Position.objects.all()
    departments = Department.objects.all()
    if request.POST:
      id = request.POST.get('leave')
      emp = Profile.objects.get(user__id=id)
      emp.end_date = datetime.now().date()
      emp.save()
      messages.success(request, 'Đã cho thằng này cút')
    keyword = request.GET.get('keyword', '')
    position = request.GET.get('position', '')
    start_date = request.GET.get('start-date', '')
    end_date = request.GET.get('end-date', '')
    department = request.GET.get('department', '')
    if keyword:
      emps = emps.filter(username__icontains=keyword)
    if position:
      emps = emps.filter(profile__position__name=position)
    if department:
      emps = emps.filter(profile__department__name=department)
    if start_date and end_date:
      emps = emps.filter(start_date__range=[start_date, end_date])
    elif start_date:
      emps = emps.filter(start_date__range=[start_date, datetime.now().date()])
    elif end_date:
      emps = emps.filter(start_date__range=[datetime.now().date(), end_date])
    paginator = Paginator(emps, 3)
    page_number = request.GET.get('page', '')
    try:
      page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
      page_obj = paginator.page(1)
    except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
    query_params = request.GET.copy()
    if 'page' in query_params:
      query_params.pop('page')
    context = {'title': title,
               'page_obj': page_obj,
               'positions': positions,
               'departments': departments,
               'position': position,
               'department': department,
               'keyword': keyword,
               'start_date': start_date,
               'end_date': end_date}
    return render(request, 'pages/employee.html', context)
  else:
    messages.warning(request, 'Không có quyền truy cập')
    return redirect('/')

def main_sheet(request):
  if request.user.is_superuser:
    title = 'Bảng công'
    sheets = Sheet.objects.all().order_by('-date')
    keyword = request.GET.get('keyword', '')
    status = request.GET.get('status', '')
    start_date = request.GET.get('start-date', '')
    end_date = request.GET.get('end-date', '')
    if keyword:
      sheets = sheets.filter(user__username__icontains=keyword)
    if status:
      sheets = sheets.filter(status=status)
    if start_date and end_date:
      sheets = sheets.filter(date__range=[start_date, end_date])
    elif start_date:
      sheets = sheets.filter(date__range=[start_date, datetime.now().date()])
    elif end_date:
      sheets = sheets.filter(date__range=[datetime.now().date(), end_date])
    paginator = Paginator(sheets, 1)
    page_number = request.GET.get('page', '')
    try:
      page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
      page_obj = paginator.page(1)
    except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
    query_params = request.GET.copy()
    if 'page' in query_params:
      query_params.pop('page')
    context = {'title': title, 
               'keyword': keyword,
               'start_date': start_date,
               'end_date': end_date,
               'status': status,
               'page_obj': page_obj,
               'query_params': query_params.urlencode()}
    return render(request, 'pages/main_sheet.html', context)
  else:
    messages.warning(request, 'Không có quyền truy cập')
    return redirect('/')