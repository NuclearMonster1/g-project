from django.conf import settings
from rest_framework import serializers

from .models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = (
            "id",
            "original_name",
            "content_type",
            "size_bytes",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if value.size > max_bytes:
            raise serializers.ValidationError(
                f"File exceeds maximum size of {settings.MAX_UPLOAD_SIZE_MB} MB."
            )
        if value.size == 0:
            raise serializers.ValidationError("File is empty.")
        return value
