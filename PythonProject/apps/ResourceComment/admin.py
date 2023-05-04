from django.contrib import admin
from apps.ResourceComment.models import ResourceComment

# Register your models here.

admin.site.register(ResourceComment,admin.ModelAdmin)