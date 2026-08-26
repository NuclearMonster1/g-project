import uuid

from django.db import models


class ScanResult(models.Model):
    class Classification(models.TextChoices):
        CLEAN = "clean", "Clean"
        MALICIOUS = "malicious", "Malicious"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.OneToOneField(
        "files.UploadedFile", on_delete=models.CASCADE, related_name="scan_result"
    )
    classification = models.CharField(max_length=10, choices=Classification.choices)
    confidence = models.FloatField()
    reasons = models.JSONField(default=list)
    model_version = models.CharField(max_length=64, default="heuristic-v1.0")
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.original_name}: {self.classification} ({self.confidence})"

    @property
    def recommended_action(self):
        if self.classification == self.Classification.MALICIOUS:
            return "Scan flagged this file. Review the report before using it."
        return "No threats were found."


class SecurityReport(models.Model):
    """US-6.0.0.0 — Human-readable security report per scan."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scan_result = models.OneToOneField(
        ScanResult, on_delete=models.CASCADE, related_name="report"
    )
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.scan_result.file.original_name}"
