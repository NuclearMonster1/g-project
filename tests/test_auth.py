import pytest
from django.urls import reverse

from apps.accounts.models import User


@pytest.mark.django_db
class TestRegistration:
    def test_register_creates_active_user(self, api_client):
        res = api_client.post(
            reverse("register"),
            {"email": "new@test.com", "password": "securepass1"},
            format="json",
        )
        assert res.status_code == 201
        user = User.objects.get(email="new@test.com")
        assert user.is_active is True

    def test_duplicate_email_rejected(self, api_client, user):
        res = api_client.post(
            reverse("register"),
            {"email": user.email, "password": "securepass1"},
            format="json",
        )
        assert res.status_code == 400


@pytest.mark.django_db
class TestLogin:
    def test_login_returns_jwt(self, api_client, user):
        res = api_client.post(
            reverse("login"),
            {"email": user.email, "password": "testpass123"},
            format="json",
        )
        assert res.status_code == 200
        assert "access" in res.data

    def test_invalid_credentials_rejected(self, api_client, user):
        res = api_client.post(
            reverse("login"),
            {"email": user.email, "password": "wrong"},
            format="json",
        )
        assert res.status_code == 401


@pytest.mark.django_db
class TestFirebaseAuth:
    def test_firebase_config_reports_unconfigured(self, api_client, settings):
        settings.FIREBASE_API_KEY = ""
        settings.FIREBASE_PROJECT_ID = ""
        res = api_client.get(reverse("firebase-config"))
        assert res.status_code == 200
        assert res.data["configured"] is False

    def test_firebase_signup_creates_user(self, api_client, monkeypatch):
        from apps.accounts import views as accounts_views

        monkeypatch.setattr(
            accounts_views,
            "verify_id_token",
            lambda token: {"email": "firebase@test.com", "uid": "uid-123", "email_verified": False},
        )
        res = api_client.post(
            reverse("firebase-auth"),
            {"idToken": "fake-token"},
            format="json",
        )
        assert res.status_code == 201
        assert "access" in res.data
        user = User.objects.get(email="firebase@test.com")
        assert user.firebase_uid == "uid-123"
