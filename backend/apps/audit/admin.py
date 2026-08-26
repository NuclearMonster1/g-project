from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "actor", "action", "file")
    list_filter = ("action",)
    search_fields = ("actor__email", "file__original_name")
    readonly_fields = ("id", "timestamp", "actor", "action", "file", "metadata")

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
