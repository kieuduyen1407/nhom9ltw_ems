from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='management'),
    path('employee/', views.employee, name='employee'),
    path('sheet/', views.main_sheet, name='main-sheet')
]