from django.db import connection

from apps.scanning.models import ScanResult, SecurityReport

from .models import UploadedFile


def _file_id_hex(file_obj):
    return str(file_obj.pk).replace("-", "")


def _clear_old_audit_refs(file_obj):
    """Remove legacy audit rows that block file deletion in SQLite."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM audit_auditlog WHERE file_id = %s",
                [_file_id_hex(file_obj)],
            )
    except Exception:
        pass


def delete_uploaded_file(file_obj: UploadedFile):
    """Delete scan data, legacy audit refs, storage file, and DB record."""
    try:
        scan = ScanResult.objects.get(file=file_obj)
    except ScanResult.DoesNotExist:
        scan = None

    if scan is not None:
        SecurityReport.objects.filter(scan_result=scan).delete()
        scan.delete()

    _clear_old_audit_refs(file_obj)
    file_obj.delete_storage()
    file_obj.delete()
