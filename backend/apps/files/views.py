from django.http import FileResponse, Http404
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.scanning.services import run_scan_for_file

from .models import UploadedFile
from .serializers import FileUploadSerializer, UploadedFileSerializer
from .services import delete_uploaded_file


class FileListView(generics.ListAPIView):
    serializer_class = UploadedFileSerializer

    def get_queryset(self):
        return UploadedFile.objects.filter(owner=self.request.user).order_by("-created_at")


class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded = serializer.validated_data["file"]
        raw_bytes = uploaded.read()

        file_obj = UploadedFile.encrypt_and_save(
            owner_id=request.user.id,
            original_name=uploaded.name,
            content_type=uploaded.content_type,
            raw_bytes=raw_bytes,
        )

        run_scan_for_file(file_obj)
        file_obj.refresh_from_db()

        return Response(
            UploadedFileSerializer(file_obj).data,
            status=status.HTTP_201_CREATED,
        )


class FileDetailView(generics.RetrieveAPIView):
    serializer_class = UploadedFileSerializer
    lookup_field = "id"

    def get_queryset(self):
        return UploadedFile.objects.filter(owner=self.request.user)


class FileDownloadView(APIView):
    def get(self, request, file_id):
        try:
            file_obj = UploadedFile.objects.get(id=file_id, owner=request.user)
        except UploadedFile.DoesNotExist:
            raise Http404("File not found.")

        if file_obj.status == UploadedFile.Status.SCANNING:
            return Response(
                {"detail": "File is still being scanned. Try again in a moment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            content = file_obj.decrypt_content()
        except ValueError:
            return Response(
                {"detail": "Failed to read file."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        from io import BytesIO

        buffer = BytesIO(content)
        response = FileResponse(buffer, as_attachment=True, filename=file_obj.original_name)
        response["Content-Type"] = file_obj.content_type
        return response


class FileDeleteView(APIView):
    def delete(self, request, file_id):
        try:
            file_obj = UploadedFile.objects.get(id=file_id, owner=request.user)
        except UploadedFile.DoesNotExist:
            raise Http404("File not found.")

        delete_uploaded_file(file_obj)
        return Response({"detail": "File deleted."}, status=status.HTTP_200_OK)
