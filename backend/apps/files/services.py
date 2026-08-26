from apps.scanning.models import ScanResult, SecurityReport

from .models import UploadedFile


def delete_uploaded_file(file_obj: UploadedFile):
    """Delete scan data, storage file, and DB record."""
    try:
        scan = ScanResult.objects.get(file=file_obj)
    except ScanResult.DoesNotExist:
        scan = None

    if scan is not None:
        SecurityReport.objects.filter(scan_result=scan).delete()
        scan.delete()

    file_obj.delete_storage()
    file_obj.delete()
