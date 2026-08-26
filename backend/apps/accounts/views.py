from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .firebase import (
    FirebaseError,
    firebase_web_config,
    get_or_create_django_user,
    tokens_for_user,
    verify_id_token,
)
from .serializers import RegisterSerializer, UserSerializer


class LoginThrottle(AnonRateThrottle):
    scope = "login"


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Account created. You can log in now.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    throttle_classes = [] if settings.DEBUG else [LoginThrottle]


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class FirebaseConfigView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(firebase_web_config())


class FirebaseAuthView(APIView):
    """Create or log in a Django user after Firebase email/password auth."""
    permission_classes = [AllowAny]

    def post(self, request):
        id_token = request.data.get("idToken") or request.data.get("id_token")
        try:
            firebase_user = verify_id_token(id_token)
            user, created = get_or_create_django_user(
                email=firebase_user["email"],
                firebase_uid=firebase_user["uid"],
            )
        except FirebaseError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        data = tokens_for_user(user)
        data["user"] = UserSerializer(user).data
        data["created"] = created
        return Response(data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
