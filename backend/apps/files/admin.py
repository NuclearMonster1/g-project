from django.contrib import admin

from .models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ("original_name", "owner", "status", "size_bytes", "created_at")
    list_filter = ("status",)
    search_fields = ("original_name", "owner__email")
