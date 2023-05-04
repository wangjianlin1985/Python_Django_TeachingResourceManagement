from django.contrib import admin
from apps.ResourceType.models import ResourceType

# Register your models here.

admin.site.register(ResourceType,admin.ModelAdmin)