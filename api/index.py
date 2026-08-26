import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"

os.environ.setdefault("VERCEL", "1")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

for folder in (str(BACKEND), str(ROOT)):
    if folder not in sys.path:
        sys.path.insert(0, folder)

for folder in ("/tmp/storage", "/tmp/media", str(BACKEND / "staticfiles")):
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError:
        pass

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
