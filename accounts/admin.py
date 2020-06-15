from django.contrib import admin

# Register your models here.

from .models import Profile, Payment

admin.site.register(Profile)
admin.site.register(Payment)