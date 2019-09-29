from django.contrib import admin

from .models import Challenge, Week, Module

# Register your models here.
admin.site.register(Challenge)
admin.site.register(Week)
admin.site.register(Module)