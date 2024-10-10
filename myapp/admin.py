from django.contrib import admin
from .models import Profile, Position,Sheet,Department

# Register your models here.
admin.site.register(Profile)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Sheet)