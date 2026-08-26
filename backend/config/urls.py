"""Root URL configuration."""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/files/", include("apps.files.urls")),
    path("api/scanning/", include("apps.scanning.urls")),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("login/", RedirectView.as_view(url="/", permanent=False), name="login-page"),
    path("signup/", TemplateView.as_view(template_name="signup.html"), name="signup-page"),
    path("dashboard/", TemplateView.as_view(template_name="dashboard.html"), name="dashboard"),
]
