from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Board)
admin.site.register(List)
admin.site.register(Task)
admin.site.register(Comment)