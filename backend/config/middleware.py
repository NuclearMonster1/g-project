from django.conf import settings
from django.core.management import call_command


class VercelStartupMiddleware:
    """Run migrations once on first request in serverless /tmp storage."""

    _ready = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not VercelStartupMiddleware._ready and getattr(settings, "IS_VERCEL", False):
            VercelStartupMiddleware._ready = True
            try:
                call_command("migrate", "--noinput", verbosity=0)
            except Exception:
                pass
        return self.get_response(request)
