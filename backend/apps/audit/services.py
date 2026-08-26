from .models import AuditLog


def log_event(actor, action, file=None, metadata=None):
    AuditLog.objects.create(
        actor=actor,
        action=action,
        file=file,
        metadata=metadata or {},
    )
