import uuid

from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """US-9.0.0.0 — Append-only audit log."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_events",
    )
    action = models.CharField(max_length=32)
    file = models.ForeignKey(
        "files.UploadedFile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_events",
    )
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        actor = self.actor.email if self.actor else "system"
        return f"{self.timestamp} | {actor} | {self.action}"

    def save(self, *args, **kwargs):
        if self.pk and AuditLog.objects.filter(pk=self.pk).exists():
            raise ValueError("Audit log entries are immutable and cannot be updated.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("Audit log entries cannot be deleted.")
