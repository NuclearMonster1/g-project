from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    actor_email = serializers.EmailField(source="actor.email", read_only=True, default=None)
    file_name = serializers.CharField(source="file.original_name", read_only=True, default=None)

    class Meta:
        model = AuditLog
        fields = (
            "id",
            "timestamp",
            "actor_email",
            "action",
            "file_name",
            "metadata",
        )
