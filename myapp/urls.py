from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('profile/',views.profile),
    path('profile/<int:id>/',views.profile_detail),
    path('about/',views.about)
]