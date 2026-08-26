from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.files.models import UploadedFile

from .models import ScanResult, SecurityReport
from .serializers import SecurityReportSerializer


class FileReportView(generics.RetrieveAPIView):
    """Security report for a scanned file (informational only)."""
    serializer_class = SecurityReportSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        file_id = self.kwargs["file_id"]
        file_obj = UploadedFile.objects.get(id=file_id, owner=self.request.user)
        scan = ScanResult.objects.get(file=file_obj)
        return SecurityReport.objects.get(scan_result=scan)
