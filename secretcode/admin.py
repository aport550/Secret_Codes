from django.contrib import admin

from .models import User
from .models import Hint

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ['username', 'password', 'secret']

@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
	list_display = ['username', 'hint']