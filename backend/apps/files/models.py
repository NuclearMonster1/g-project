import base64
import hashlib
import os
import uuid

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.db import models


def _get_fernet():
    key = settings.FILE_ENCRYPTION_KEY.encode()
    digest = hashlib.sha256(key).digest()
    fernet_key = base64.urlsafe_b64encode(digest)
    return Fernet(fernet_key)


class UploadedFile(models.Model):
    class Status(models.TextChoices):
        UPLOADING = "uploading", "Uploading"
        SCANNING = "scanning", "Scanning"
        CLEAN = "clean", "Clean"
        QUARANTINED = "quarantined", "Quarantined"
        FAILED = "failed", "Failed"
        DELETED = "deleted", "Deleted"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="files"
    )
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=128, blank=True)
    size_bytes = models.BigIntegerField(default=0)
    storage_path = models.CharField(max_length=512)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SCANNING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.original_name} ({self.status})"

    @staticmethod
    def encrypt_and_save(owner_id, original_name, content_type, raw_bytes):
        file_id = uuid.uuid4()
        storage_dir = settings.STORAGE_ROOT / str(owner_id)
        storage_dir.mkdir(parents=True, exist_ok=True)
        storage_path = storage_dir / f"{file_id}.enc"

        fernet = _get_fernet()
        encrypted = fernet.encrypt(raw_bytes)
        with open(storage_path, "wb") as f:
            f.write(encrypted)

        return UploadedFile.objects.create(
            id=file_id,
            owner_id=owner_id,
            original_name=original_name,
            content_type=content_type or "application/octet-stream",
            size_bytes=len(raw_bytes),
            storage_path=str(storage_path),
            status=UploadedFile.Status.SCANNING,
        )

    def decrypt_content(self):
        fernet = _get_fernet()
        with open(self.storage_path, "rb") as f:
            encrypted = f.read()
        try:
            return fernet.decrypt(encrypted)
        except InvalidToken as exc:
            raise ValueError("Failed to decrypt file") from exc

    def delete_storage(self):
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)
