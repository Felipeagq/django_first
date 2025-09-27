from django.contrib import admin
from .models import Role, User,UserType
# Register your models here.

admin.site.register(Role)
admin.site.register(UserType)
admin.site.register(User)

