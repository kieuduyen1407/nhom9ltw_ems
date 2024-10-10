from datetime import datetime, time
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

# Create your models here.
class Position(models.Model):
    name=models.CharField(max_length=50)
    salary_coef=models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField()

    def __str__(self):
        return self.name


class Department(models.Model):
    name=models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class Profile(models.Model):
    dob=models.DateField()
    phone_number=models.CharField(max_length=12)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    position=models.ForeignKey(Position,on_delete=models.CASCADE, default=1)
    gender = models.CharField(max_length=10, choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')])
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
         return f'Profile: {self.user.username}'

# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         user_profile = Profile(user=instance)
#         user_profile.save()
#
# post_save.connect(create_profile, sender=User)


class Sheet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    checkin=models.TimeField()
    checkout=models.TimeField(blank=True, null=True)
    work_hour=models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    salary=models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    status=models.CharField(max_length=20, choices=[('Đúng Giờ', 'Đúng Giờ'), ('Muộn', 'Muộn')], default='Đúng Giờ')

    def __str__(self):
        return f'{self.user.username} - {self.date}'

    def is_late(self):
        if self.checkin > time(8, 0, 0):
            self.status = 'Muộn'

    def calculate_salary(self):
        profile = Profile.objects.get(user=self.user)
        if self.work_hour is not None:
            if self.status == 'Muộn':
                salary_1hour = 25000
            else:
                salary_1hour = 30000
            rate = profile.position.salary_coef * salary_1hour
            self.salary = rate * Decimal(self.work_hour)
        else:
            self.salary = 0

    def save(self, *args, **kwargs):
        if self.checkin and self.checkout:
            checkin = timezone.datetime.combine(self.date, self.checkin)
            checkout = timezone.datetime.combine(self.date, self.checkout)
            self.work_hour = (checkout - checkin).seconds/3600

        self.is_late()
        self.calculate_salary()
        super().save( *args, **kwargs)