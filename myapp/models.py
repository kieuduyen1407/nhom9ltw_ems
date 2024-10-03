from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Position(models.Model):
    name=models.CharField(max_length=50)
    salary_coef=models.IntegerField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    nickname=models.CharField(max_length=50)
    dob=models.DateField(null=True, blank=True)
    phone_number=models.CharField(max_length=12)
    position=models.ForeignKey(Position,on_delete=models.CASCADE, default=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
         return f'{self.nickname} - {self.user.username}'

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.user.username
        super(Profile, self).save(*args, **kwargs)

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)



class Sheet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    checkin=models.TimeField()
    checkout=models.TimeField()
    work_hour=models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    salary=models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    status=models.CharField(max_length=20, choices=[('Đúng Giờ', 'Đúng Giờ'), ('Muộn', 'Muộn')], default='Đúng Giờ')

    def __str__(self):
        return f'{self.user.username} - {self.date}'

    def calculate_salary(self):
        profile = Profile.objects.get(user=self.user)
        rate = profile.position.salary_coef * 60000
        if self.work_hour is not None:
            self.salary = rate * self.work_hour
        else:
            self.salary = 0

