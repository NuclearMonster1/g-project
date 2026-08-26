from rest_framework import serializers

from .models import ScanResult, SecurityReport


class ScanResultSerializer(serializers.ModelSerializer):
    recommended_action = serializers.CharField(read_only=True)
    file_id = serializers.UUIDField(source="file.id", read_only=True)
    file_name = serializers.CharField(source="file.original_name", read_only=True)

    class Meta:
        model = ScanResult
        fields = (
            "id",
            "file_id",
            "file_name",
            "classification",
            "confidence",
            "reasons",
            "model_version",
            "scanned_at",
            "recommended_action",
        )


class SecurityReportSerializer(serializers.ModelSerializer):
    scan_result = ScanResultSerializer(read_only=True)
    file_id = serializers.UUIDField(source="scan_result.file_id", read_only=True)
    file_name = serializers.CharField(source="scan_result.file.original_name", read_only=True)

    class Meta:
        model = SecurityReport
        fields = (
            "id",
            "file_id",
            "file_name",
            "summary",
            "scan_result",
            "created_at",
        )
