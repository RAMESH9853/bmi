from django.contrib import admin
from .models import Profile


# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display = ['user','full_name','gender','height','weight','bmi']

admin.site.register(Profile , AdminUser)
