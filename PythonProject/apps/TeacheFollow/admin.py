from django.contrib import admin
from apps.TeacheFollow.models import TeacheFollow

# Register your models here.

admin.site.register(TeacheFollow,admin.ModelAdmin)