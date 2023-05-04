from django.contrib import admin
from apps.Collection.models import Collection

# Register your models here.

admin.site.register(Collection,admin.ModelAdmin)