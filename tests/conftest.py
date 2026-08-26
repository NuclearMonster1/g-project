import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User


@pytest.fixture(autouse=True)
def configure_test_settings(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path / "media"
    settings.STORAGE_ROOT = tmp_path / "storage"
    settings.STORAGE_ROOT.mkdir(parents=True, exist_ok=True)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email="user@test.com", password="testpass123")
