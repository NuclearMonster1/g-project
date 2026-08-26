from django.contrib import admin

from .models import ScanResult, SecurityReport


@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ("file", "classification", "confidence", "scanned_at")
    list_filter = ("classification",)


@admin.register(SecurityReport)
class SecurityReportAdmin(admin.ModelAdmin):
    list_display = ("scan_result", "created_at")
