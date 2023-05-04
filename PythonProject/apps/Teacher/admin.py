from django.contrib import admin
from apps.Teacher.models import Teacher

# Register your models here.

admin.site.register(Teacher,admin.ModelAdmin)