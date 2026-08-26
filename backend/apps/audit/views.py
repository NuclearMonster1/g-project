from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsAdminUser
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogListView(generics.ListAPIView):
    """US-9.0.0.0 — Admin audit log with filters."""
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        qs = AuditLog.objects.select_related("actor", "file").all()
        user_id = self.request.query_params.get("user_id")
        file_id = self.request.query_params.get("file_id")
        action = self.request.query_params.get("action")

        if user_id:
            qs = qs.filter(actor_id=user_id)
        if file_id:
            qs = qs.filter(file_id=file_id)
        if action:
            qs = qs.filter(action=action)
        return qs
