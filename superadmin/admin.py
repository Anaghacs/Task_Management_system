from django.contrib import admin

# Register your models here.
from .models import UserProfile, Task, TaskDetails

admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(TaskDetails)