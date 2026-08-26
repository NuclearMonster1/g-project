import pytest
from django.urls import reverse

from apps.files.models import UploadedFile


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


EICAR = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"


@pytest.mark.django_db
class TestFileUpload:
    def test_upload_clean_file(self, auth_client):
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile

        f = SimpleUploadedFile("notes.txt", b"hello world", content_type="text/plain")
        res = auth_client.post(reverse("file-upload"), {"file": f}, format="multipart")
        assert res.status_code == 201
        assert res.data["status"] == UploadedFile.Status.CLEAN

    def test_upload_eicar_still_downloadable(self, auth_client):
        from django.core.files.uploadedfile import SimpleUploadedFile

        f = SimpleUploadedFile("eicar.com", EICAR, content_type="application/octet-stream")
        res = auth_client.post(reverse("file-upload"), {"file": f}, format="multipart")
        assert res.status_code == 201
        assert res.data["status"] == UploadedFile.Status.CLEAN

        download = auth_client.get(reverse("file-download", kwargs={"file_id": res.data["id"]}))
        assert download.status_code == 200


@pytest.mark.django_db
class TestDelete:
    def test_delete_own_file(self, auth_client):
        from django.core.files.uploadedfile import SimpleUploadedFile

        f = SimpleUploadedFile("temp.txt", b"delete me", content_type="text/plain")
        upload = auth_client.post(reverse("file-upload"), {"file": f}, format="multipart")
        file_id = upload.data["id"]

        res = auth_client.delete(reverse("file-delete", kwargs={"file_id": file_id}))
        assert res.status_code == 200
        assert not UploadedFile.objects.filter(id=file_id).exists()

    def test_delete_quarantined_status_file(self, auth_client):
        from django.core.files.uploadedfile import SimpleUploadedFile

        f = SimpleUploadedFile("old.exe", EICAR, content_type="application/octet-stream")
        upload = auth_client.post(reverse("file-upload"), {"file": f}, format="multipart")
        file_id = upload.data["id"]

        UploadedFile.objects.filter(id=file_id).update(status=UploadedFile.Status.QUARANTINED)

        res = auth_client.delete(reverse("file-delete", kwargs={"file_id": file_id}))
        assert res.status_code == 200
        assert not UploadedFile.objects.filter(id=file_id).exists()
