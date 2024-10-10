from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name = 'login'),
    path('register/',views.register, name = 'register'),
    path('logout/', views.logout),
    path('update_info/<str:username>/', views.update_info),
    path('time-keeping/', views.time_keeping, name='time-keeping'),
    path('sheet/<str:username>/', views.sheet, name='sheet'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail')
]