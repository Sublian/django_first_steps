from django.contrib import admin
from .models import Proyect, Task

# Register your models here.
class TaskAmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    
admin.site.register(Proyect)
admin.site.register(Task, TaskAmin)