from django.urls import path

from .views import FileDeleteView, FileDetailView, FileDownloadView, FileListView, FileUploadView

urlpatterns = [
    path("", FileListView.as_view(), name="file-list"),
    path("upload/", FileUploadView.as_view(), name="file-upload"),
    path("<uuid:id>/", FileDetailView.as_view(), name="file-detail"),
    path("<uuid:file_id>/download/", FileDownloadView.as_view(), name="file-download"),
    path("<uuid:file_id>/delete/", FileDeleteView.as_view(), name="file-delete"),
]
