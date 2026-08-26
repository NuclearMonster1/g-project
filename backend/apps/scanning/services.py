import sys
from pathlib import Path

from django.conf import settings

from apps.files.models import UploadedFile

from .models import ScanResult, SecurityReport

PROJECT_ROOT = Path(settings.BASE_DIR).parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.inference import scan_bytes  # noqa: E402


def _build_report_summary(scan_result: ScanResult) -> str:
    label = scan_result.classification.title()
    reasons = "; ".join(scan_result.reasons) if scan_result.reasons else "No details."
    return (
        f"Classification: {label} | "
        f"Confidence: {scan_result.confidence * 100:.1f}% | "
        f"Reasons: {reasons}"
    )


def run_scan_for_file(file_obj: UploadedFile):
    """Run malware scan and save report. File stays downloadable after scan."""
    file_obj.status = UploadedFile.Status.SCANNING
    file_obj.save(update_fields=["status", "updated_at"])

    raw = file_obj.decrypt_content()
    result = scan_bytes(raw, filename=file_obj.original_name)

    classification = (
        ScanResult.Classification.MALICIOUS
        if result.classification == "malicious"
        else ScanResult.Classification.CLEAN
    )

    scan_result, _ = ScanResult.objects.update_or_create(
        file=file_obj,
        defaults={
            "classification": classification,
            "confidence": result.confidence,
            "reasons": result.reasons,
            "model_version": result.model_version,
        },
    )

    SecurityReport.objects.update_or_create(
        scan_result=scan_result,
        defaults={"summary": _build_report_summary(scan_result)},
    )

    file_obj.status = UploadedFile.Status.CLEAN
    file_obj.save(update_fields=["status", "updated_at"])

    return scan_result
