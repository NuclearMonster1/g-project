from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "firebase_uid", "is_active", "created_at")
    search_fields = ("email", "firebase_uid")
