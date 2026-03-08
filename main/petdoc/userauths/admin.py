
from django.contrib import admin

# Register your models here.
from userauths.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio','is_staff']


admin.site.register(User, UserAdmin)
