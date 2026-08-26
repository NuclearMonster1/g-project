"""Verify Firebase ID tokens using the Identity Toolkit REST API."""
import json
import urllib.error
import urllib.request

from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

LOOKUP_URL = "https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={key}"


class FirebaseError(Exception):
    pass


def firebase_configured():
    return bool(settings.FIREBASE_API_KEY and settings.FIREBASE_PROJECT_ID)


def firebase_web_config():
    return {
        "apiKey": settings.FIREBASE_API_KEY,
        "authDomain": settings.FIREBASE_AUTH_DOMAIN,
        "projectId": settings.FIREBASE_PROJECT_ID,
        "appId": settings.FIREBASE_APP_ID,
        "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
        "messagingSenderId": settings.FIREBASE_MESSAGING_SENDER_ID,
        "configured": firebase_configured(),
    }


def verify_id_token(id_token):
    if not firebase_configured():
        raise FirebaseError("Firebase is not configured on the server.")
    if not id_token:
        raise FirebaseError("Missing Firebase ID token.")

    payload = json.dumps({"idToken": id_token}).encode("utf-8")
    request = urllib.request.Request(
        LOOKUP_URL.format(key=settings.FIREBASE_API_KEY),
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise FirebaseError("Invalid or expired Firebase session.") from exc
    except urllib.error.URLError as exc:
        raise FirebaseError("Could not reach Firebase. Check your internet connection.") from exc

    users = data.get("users") or []
    if not users:
        raise FirebaseError("Firebase account not found.")

    user = users[0]
    email = (user.get("email") or "").strip().lower()
    uid = user.get("localId") or ""
    if not email or not uid:
        raise FirebaseError("Firebase account is missing email.")
    return {"email": email, "uid": uid, "email_verified": bool(user.get("emailVerified"))}


def get_or_create_django_user(email, firebase_uid):
    user = User.objects.filter(firebase_uid=firebase_uid).first()
    if user:
        if user.email != email:
            user.email = email
            user.save(update_fields=["email"])
        return user, False

    user = User.objects.filter(email=email).first()
    if user:
        if not user.firebase_uid:
            user.firebase_uid = firebase_uid
            user.save(update_fields=["firebase_uid"])
        return user, False

    user = User.objects.create_user(email=email, password=None, firebase_uid=firebase_uid)
    return user, True


def tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
