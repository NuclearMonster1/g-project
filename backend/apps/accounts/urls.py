from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import FirebaseAuthView, FirebaseConfigView, LoginView, MeView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("firebase/", FirebaseAuthView.as_view(), name="firebase-auth"),
    path("firebase-config/", FirebaseConfigView.as_view(), name="firebase-config"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
]
