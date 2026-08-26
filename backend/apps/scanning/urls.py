from django.urls import path

from .views import FileReportView

urlpatterns = [
    path("report/<uuid:file_id>/", FileReportView.as_view(), name="file-report"),
]
