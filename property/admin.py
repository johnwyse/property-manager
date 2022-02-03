from django.contrib import admin
from .models import User, Message, Unit, Issue

# Register your models here.
admin.site.register(User)
admin.site.register(Message)
admin.site.register(Issue)
admin.site.register(Unit)