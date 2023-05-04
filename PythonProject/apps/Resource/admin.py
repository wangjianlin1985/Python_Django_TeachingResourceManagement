from django.contrib import admin
from apps.Resource.models import Resource

# Register your models here.

admin.site.register(Resource,admin.ModelAdmin)